"""
脚本名称: mamba_dataset.py
版本: V1.1
最后修改时间: 2026-03-30

功能概述:
1) 读取 MATLAB v7.3 (HDF5) 导出的 Mamba 数据集文件。
2) 提供 PyTorch Dataset 接口，支持 train/val/test 三个 split。
3) 采用 HDF5 延迟打开策略，兼容 DataLoader 多进程加载。

输入文件约定:
- X_{split}: [D, L, N] (MATLAB 保存后的维度顺序)
- Y_{split}_theta / delta / main / turn / slip / stall: [L, N]
- mu / sigma: 通道级归一化统计量

输出约定 (__getitem__):
- x: FloatTensor [L, D]
- y_theta, y_delta: FloatTensor [L]
- y_main, y_turn, y_slip, y_stall: LongTensor [L]
"""

import h5py
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class MambaAGVDataset(Dataset):
    """
    函数名/类名: MambaAGVDataset
    功能:
    - AGV Mamba 训练数据集加载器 (适配 MATLAB v7.3 HDF5 导出格式)。
    - 支持 DataLoader 多工作进程 (num_workers > 0)。

    设计要点:
    - 仅在 worker 首次取样时打开 HDF5 句柄，避免主进程提前持有文件句柄导致卡死。
    - 单次按索引读取单个窗口，避免一次性加载全量数据引发内存压力。
    """

    def __init__(self, mat_file_path: str, split: str = 'train'):
        """
        函数: __init__
        功能: 初始化数据集并完成元信息探测。

        参数:
        - mat_file_path (str): Mamba_dataset_export.mat 的路径。
        - split (str): 数据划分标识，可选 'train' / 'val' / 'test'。

        返回:
        - 无。初始化对象内部状态。

        异常:
        - AssertionError: split 取值非法。
        - RuntimeError: HDF5 文件读取失败或关键键缺失。
        """
        assert split in ['train', 'val', 'test'], "Split 必须是 train, val 或 test"
        self.split = split
        self.file_path = mat_file_path
        self.h5_file = None  # 延迟打开，解决多进程下 DataLoader 卡死报错的问题
        
        # 1. 尝试临时打开 HDF5 文件探测元数据
        try:
            with h5py.File(self.file_path, 'r') as f:
                # 读取基本元数据
                self.mu = np.array(f['mu']).squeeze()
                self.sigma = np.array(f['sigma']).squeeze()
                
                # 记录核心样本数 (由 X 张量的最后一维决定)
                self.num_samples = f[f'X_{split}'].shape[-1]
                
        except Exception as e:
            raise RuntimeError(f"无法读取 HDF5 文件 {self.file_path}，报错: {e}")
            
        # MATLAB 复杂的字符串反解往往不可靠，直接提供硬件编码的兜底名
        self.channels = ['accel_x', 'gyro_y', 'gyro_z', 'I_lf', 'I_rr', 
                         'omega_w_lf', 'omega_w_rr', 'slip_lf', 'slip_rr', 'accel_y']

        print(f"✅ 成功加载 {split.upper()} 集，共包含 {self.num_samples} 个滑动窗口。")

    def __len__(self):
        """
        函数: __len__
        功能: 返回当前 split 的样本总数。

        返回:
        - int: 滑动窗口数量。
        """
        return self.num_samples

    def __getitem__(self, idx):
        """
        函数: __getitem__
        功能: 按样本索引读取一个时间窗样本及其多头标签。

        参数:
        - idx (int): 样本索引，范围 [0, len(self)-1]。

        返回:
        - dict:
          - 'x': FloatTensor [L, D]
          - 'y_theta': FloatTensor [L]
          - 'y_delta': FloatTensor [L]
          - 'y_main' / 'y_turn' / 'y_slip' / 'y_stall': LongTensor [L]

        说明:
        - MATLAB 导出的 X 为 [D, L, N]，此处取 [:, :, idx] 后转置为 [L, D]。
        """
        # 延迟绑定核心数据引用：只有 worker 进程拿索引时才会打开句柄，打破多进程堵塞
        if self.h5_file is None:
            self.h5_file = h5py.File(self.file_path, 'r')
            
            self.X_ref = self.h5_file[f'X_{self.split}']
            self.Y_theta_ref = self.h5_file[f'Y_{self.split}_theta']
            self.Y_delta_ref = self.h5_file[f'Y_{self.split}_delta']
            self.Y_main_ref  = self.h5_file[f'Y_{self.split}_main']
            self.Y_turn_ref  = self.h5_file[f'Y_{self.split}_turn']
            self.Y_slip_ref  = self.h5_file[f'Y_{self.split}_slip']
            self.Y_stall_ref = self.h5_file[f'Y_{self.split}_stall']

        # HDF5 加载：只读取需要的那一个窗口，防内存溢出
        # 因 MATLAB 转置机制，取的是 [:, :, idx] 然后 transpose 变回 [L, D]
        x = self.X_ref[:, :, idx].transpose(1, 0)
        
        # 标签 (回归与分类)
        return {
            'x': torch.from_numpy(x).float(),
            'y_theta': torch.from_numpy(self.Y_theta_ref[:, idx]).float(),
            'y_delta': torch.from_numpy(self.Y_delta_ref[:, idx]).float(),
            'y_main': torch.from_numpy(self.Y_main_ref[:, idx]).long(),
            'y_turn': torch.from_numpy(self.Y_turn_ref[:, idx]).long(),
            'y_slip': torch.from_numpy(self.Y_slip_ref[:, idx]).long(),
            'y_stall': torch.from_numpy(self.Y_stall_ref[:, idx]).long()
        }

    def close(self):
        """
        函数: close
        功能: 释放 HDF5 文件句柄，建议在训练结束或数据集对象销毁前调用。

        返回:
        - 无。
        """
        if self.h5_file is not None:
            self.h5_file.close()
            self.h5_file = None

if __name__ == "__main__":
    """
    自检入口:
    - 用于快速验证数据文件可读取、DataLoader 可工作以及张量维度是否符合预期。
    - 正式训练时通常由训练脚本导入 MambaAGVDataset，而不是执行本文件主入口。
    """

    # 测试读取脚本
    mat_path = r"../../data/mamba/Mamba_dataset_export.mat"
    
    try:
        # 初始化 Dataset
        train_dataset = MambaAGVDataset(mat_path, split='train')
        
        # DataLoader 使用 (设置 num_workers > 0 验证多进程能力)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
        
        # 抽样提取
        for batch in train_loader:
            x = batch['x']
            print("🚀 首个 Batch 的输入维度 (B, L, D):", x.shape)
            print("坡度回归标签维度 (B, L):", batch['y_theta'].shape)
            print("打滑分类标签维度 (B, L):", batch['y_slip'].shape)
            break
            
        train_dataset.close()
    except Exception as e:
        print("遇到错误:", e)
