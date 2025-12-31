% =============================
% 文件名：GRU_infer.m
% 版本号：V1.1（简化主分类：3类，移除 slip）
% 最后修改时间：2025-12-30
% 作者：LPV-MPC Project
% 功能描述：
%   GRU单步推理接口
%   输入一个序列，输出三个任务的预测结果
%
% 输入参数：
%   - x_seq: 输入序列 [seq_len, feat_dim] 或 [feat_dim, seq_len, 1]
%   - model: 模型结构体（从 GRU_model.mat 加载）
%
% 输出参数：
%   - label_main: 主分类标签 ∈ {1,2,3} (flat/stall/slope)
%   - label_turn: 转弯状态标签 ∈ {-1,0,+1} (right/straight/left)
%   - theta_hat: 坡度角估计 [rad]
%   - conf: 置信度结构体
%     .conf_main: 主分类置信度 [3×1]
%     .conf_turn: 转弯分类置信度 [3×1]
%     .label_main_name: 主分类标签名称
%     .label_turn_name: 转弯状态标签名称
%
% 依赖：
%   - GRU_model.mat（由 GRU_train.m 生成）
%
% 备注：
%   - 输入序列需已归一化（使用model.scaler）
%   - 如需从原始传感量推理，请使用 GRU_state_classifier.m
% =============================

function [label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model)
%GRU_INFER GRU单步推理接口
%
% 示例:
%   load('GRU_model.mat', 'model');
%   x_seq = randn(96, 16);  % [seq_len, feat_dim]
%   [label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model);

    %% 输入验证
    if nargin < 2
        error('需要提供输入序列和模型: GRU_infer(x_seq, model)');
    end
    
    % 检查输入维度
    if size(x_seq, 1) == model.net_feature.Layers(1).InputSize && ...
       size(x_seq, 2) > 1
        % [feat_dim, seq_len] → [feat_dim, seq_len, 1]
        x_seq = reshape(x_seq, size(x_seq, 1), size(x_seq, 2), 1);
    elseif size(x_seq, 2) == model.net_feature.Layers(1).InputSize && ...
           size(x_seq, 1) > 1
        % [seq_len, feat_dim] → [feat_dim, seq_len, 1]
        x_seq = permute(x_seq, [2, 1]);
        x_seq = reshape(x_seq, size(x_seq, 1), size(x_seq, 2), 1);
    end
    
    % 最终检查：应该是 [feat_dim, seq_len, 1]
    expected_feat_dim = model.net_feature.Layers(1).InputSize;
    if size(x_seq, 1) ~= expected_feat_dim
        error('输入序列特征维度错误: 期望 %d, 实际 %d', ...
            expected_feat_dim, size(x_seq, 1));
    end
    
    %% 转为dlarray
    X = dlarray(x_seq, 'CBT');  % [feat_dim, seq_len, 1]
    
    % 如果模型在GPU上，也将输入转到GPU
    if canUseGPU() && isa(model.fc_main_weights, 'gpuArray')
        X = gpuArray(X);
    end
    
    %% 前向传播
    % 1) GRU特征提取
    features_seq = forward(model.net_feature, X);  % [hidden_size, seq_len, 1]
    
    % 提取最后一个时间步的特征
    features = features_seq(:, end, :);  % [hidden_size, 1, 1]
    features = squeeze(features);  % [hidden_size, 1]
    
    % 移除维度标签（避免矩阵乘法时的维度标签冲突）
    features = stripdims(features);
    
    % 2) 主分类头
    logits_main = model.fc_main_weights * features + model.fc_main_bias;  % [3, 1]
    probs_main = softmax(logits_main, 'DataFormat', 'CB');
    probs_main = extractdata(gather(probs_main));  % [3, 1]
    [conf_main_max, label_main] = max(probs_main);
    
    % 3) 转弯分类头
    logits_turn = model.fc_turn_weights * features + model.fc_turn_bias;  % [3, 1]
    probs_turn = softmax(logits_turn, 'DataFormat', 'CB');
    probs_turn = extractdata(gather(probs_turn));  % [3, 1]
    [conf_turn_max, label_turn_idx] = max(probs_turn);
    
    % 映射转弯标签：{1,2,3} → {-1,0,+1}
    label_turn = label_turn_idx - 2;  % 1→-1, 2→0, 3→+1
    
    % 4) 坡度回归头
    pred_theta = model.fc_theta_weights * features + model.fc_theta_bias;  % [1, 1]
    theta_hat = extractdata(gather(pred_theta));
    
    %% 构建输出
    % 置信度结构体
    conf = struct();
    conf.conf_main = probs_main;  % [3×1]
    conf.conf_turn = probs_turn;  % [3×1]
    conf.conf_main_max = conf_main_max;
    conf.conf_turn_max = conf_turn_max;
    
    % 标签名称
    conf.label_main_name = model.class_labels_main{label_main};
    conf.label_turn_name = model.class_labels_turn{label_turn_idx};
    
    % 返回标量
    label_main = double(label_main);
    label_turn = double(label_turn);
    theta_hat = double(theta_hat);
end

