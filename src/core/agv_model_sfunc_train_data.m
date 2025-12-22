
function agv_model_sfunc_train_data(block)
% =============================
% 文件名：agv_model_sfunc_train_data.m
% 版本号：V4.6-Train
% 派生自：agv_model_sfunc.m (V4.x)
% 最后修改时间：2025-11-02
% 作者：LPV-MPC Project
% 
% 【重要】本文件专用于GRU训练数据生成！
% 与原版差异：
%   1. 输入端口从3维扩展到5维
%   2. 新增输入：slip_gamma (打滑系数), stall_load (堵转负载)
%   3. 调用训练数据专用函数：state_eq_ref_train_data, output_eq_ref_train_data
% 
% 同步策略：
%   - 如修改S-Function框架结构，需同步更新原版agv_model_sfunc.m
%   - 仅输入端口维度与调用函数名可独立修改
% 
% 用途：GRU_DataGen.slx（AI训练数据生成）
% 原版用途：LPVMPC_AGV_simulink.slx（控制系统验证）
% =============================
%
% Level-2 MATLAB S-Function (Simulink)
% 外壳：AGV 离散植物，内部调用 state_eq_ref_train_data / output_eq_ref_train_data
% 接口：
%   - 参数 p：parameters() 结构体（必须包含 Ts；可选 nx、x0）
%   - 输入端口(1)：u_all = [F_cmd; omega_cmd; theta_ground; slip_gamma; stall_load] (5x1)
%       其中：
%         slip_gamma: 打滑注入系数 (1.0=正常, 0.3-0.7=打滑)
%         stall_load: 堵转外部负载[N] (0=正常, >0=阻力)
%   - 输出端口(1)：y (31x1)
%   - 离散状态：x (nx×1，默认 8)，使用 DWork 管理
% ==========================================
setup(block);

% -------- S-Function 框架 --------
function setup(block)
  % 1) 模块参数
  block.NumDialogPrms  = 1;    % p = parameters()

  % 2) 端口
  block.NumInputPorts  = 1;
  block.NumOutputPorts = 1;

  % 输入端口：5×1 (V4.6-Train: 增加slip_gamma和stall_load)
  block.SetPreCompInpPortInfoToDynamic;
  block.InputPort(1).Dimensions        = 5;
  block.InputPort(1).DatatypeID        = 0; % double
  block.InputPort(1).Complexity        = 'Real';
  block.InputPort(1).DirectFeedthrough = false;

  % 输出端口：31×1
  block.SetPreCompOutPortInfoToDynamic;
  block.OutputPort(1).Dimensions = 31;
  block.OutputPort(1).DatatypeID = 0; % double
  block.OutputPort(1).Complexity = 'Real';

  % 3) 采样时间（来自参数 Ts）
  p = block.DialogPrm(1).Data;
  if ~isfield(p,'Ts')
      error('parameters() 必须包含字段 Ts');
  end
  block.SampleTimes = [p.Ts 0];

  % 4) 不在 setup 里设置 NumDworks / Dwork 属性

  % 5) 注册方法
  block.SimStateCompliance = 'DefaultSimState';
  block.RegBlockMethod('PostPropagationSetup', @DoPostPropSetup);
  block.RegBlockMethod('InitializeConditions', @DoInitialize);
  block.RegBlockMethod('Outputs',              @DoOutputs);
  block.RegBlockMethod('Update',               @DoUpdate);
end

% -------- 在 PostPropagationSetup 里设置 DWork 的数量和属性 --------
function DoPostPropSetup(block)
  block.NumDworks = 1;  % 关键：必须在这里设置

  % 状态维度（可用 p.nx 指定，默认 8）
  nx = 8;
  if block.NumDialogPrms>=1 && isstruct(block.DialogPrm(1).Data)
      p = block.DialogPrm(1).Data;
      if isfield(p,'nx') && ~isempty(p.nx)
          nx = p.nx;
      end
  end

  block.Dwork(1).Name            = 'xdisc';
  block.Dwork(1).Dimensions      = nx;
  block.Dwork(1).DatatypeID      = 0;     % double
  block.Dwork(1).Complexity      = 'Real';
  block.Dwork(1).UsedAsDiscState = true;  % 离散状态
end

% -------- 初始化离散状态 --------
function DoInitialize(block)
  p = block.DialogPrm(1).Data;
  nx = block.Dwork(1).Dimensions;

  % 优先使用 p.x0；否则由 parameters.m 的 initial_* 字段组装
  if isfield(p,'x0') && ~isempty(p.x0)
      x0 = p.x0(:);
  elseif all(isfield(p, {'initial_x','initial_y','initial_heading', ...
                         'initial_velocity','initial_angular_velocity', ...
                         'initial_front_steering','initial_rear_steering', ...
                         'initial_sideslip'}))
      x0 = [p.initial_x; p.initial_y; p.initial_heading; ...
            p.initial_velocity; p.initial_angular_velocity; ...
            p.initial_front_steering; p.initial_rear_steering; ...
            p.initial_sideslip];
  else
      x0 = zeros(nx,1);
  end

  if numel(x0)~=nx
      error('x0 维度(%d)与 nx(%d)不一致', numel(x0), nx);
  end
  block.Dwork(1).Data = x0;
end

% -------- 输出方程 --------
function DoOutputs(block)
  p     = block.DialogPrm(1).Data;
  u_all = block.InputPort(1).Data;       % [F_cmd; omega_cmd; theta_ground; slip_gamma; stall_load]
  x     = block.Dwork(1).Data;

  u            = u_all(1:2);             % 控制量
  theta_ground = u_all(3);               % 坡度角
  slip_gamma   = u_all(4);               % V4.6-Train: 打滑注入系数
  stall_load   = u_all(5);               % V4.6-Train: 堵转外部负载

  % 调用训练数据专用输出方程
  y = output_eq_ref_train_data(x, u, theta_ground, p, slip_gamma, stall_load);

  if ~isvector(y) || numel(y)~=block.OutputPort(1).Dimensions
      error('output_eq_ref_train_data 返回长度与输出端口不一致，期望 %d，实际 %d', ...
            block.OutputPort(1).Dimensions, numel(y));
  end
  block.OutputPort(1).Data = y(:);
end

% -------- 状态更新（离散化步进）--------
function DoUpdate(block)
  p     = block.DialogPrm(1).Data;
  u_all = block.InputPort(1).Data;       % [F_cmd; omega_cmd; theta_ground; slip_gamma; stall_load]
  x     = block.Dwork(1).Data;

  u            = u_all(1:2);
  theta_ground = u_all(3);
  slip_gamma   = u_all(4);               % V4.6-Train: 打滑注入系数
  stall_load   = u_all(5);               % V4.6-Train: 堵转外部负载

  % 调用训练数据专用状态方程
  x_next = state_eq_ref_train_data(x, u, theta_ground, p, slip_gamma, stall_load);

  if numel(x_next)~=numel(x)
      error('state_eq_ref_train_data 返回维度与 DWork 不一致');
  end
  block.Dwork(1).Data = x_next(:);
end
end


