import open3d as o3d
import numpy as np

# 1. 读取 PLY 文件

ply_path = "./yopo_sim/pointcloud-0.ply"  # 替换为你的 PLY 文件路径
# ply_path = "./yopo_sim/single_scene_data/pointcloud-0.ply"  # 替换为你的 PLY 文件路径
point_cloud = o3d.io.read_point_cloud(ply_path)

if not point_cloud:
    raise ValueError("无法读取 PLY 文件")

# 2. 转换为 NumPy 数组并过滤 Z < 6m 的点
points = np.asarray(point_cloud.points)
colors = np.asarray(point_cloud.colors) if point_cloud.has_colors() else None

# 筛选 Z < 6 的点
mask = points[:, 2] < 5.0  # Z 轴是第 3 列（索引 2）
filtered_points = points[mask]

# 创建新的点云对象
filtered_cloud = o3d.geometry.PointCloud()
filtered_cloud.points = o3d.utility.Vector3dVector(filtered_points)

# 如果有颜色，也进行过滤
if colors is not None:
    filtered_colors = colors[mask]
    filtered_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

# 3. 可视化过滤后的点云
o3d.visualization.draw_geometries(
    [filtered_cloud],
    window_name="Z < 6m 的点云",
    width=800,
    height=600,
    zoom=0.8,
)