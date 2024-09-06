from napari.utils.notifications import show_info
from napari.types import LayerDataTuple
import napari
from astropy.io import fits
import numpy as np
from qtpy.QtWidgets import QFileDialog

def show_hello_message():
    show_info('你好，世界！')
    
    filename, _ = QFileDialog.getOpenFileName(caption="选择一个文件")
    if filename:
        show_info(f'你好，世界！已选择文件：{filename}')
    else:
        show_info('你好，世界！未选择文件。')

def load_fits_file() -> LayerDataTuple:
    # 打开文件选择对话框
    filename, _ = QFileDialog.getOpenFileName(caption="选择一个FITS文件", filter="FITS files (*.fits *.fit)")
    if filename:
        with fits.open(filename) as hdul:
            # 假设我们要显示第一个HDU的数据
            data = hdul[0].data
            # 如果数据是3D的,我们可能需要选择一个切片来显示
            if data.ndim == 3:
                data = data[0]
            # 返回一个LayerDataTuple
            # 进行直方图拉伸
            p2, p98 = np.percentile(data, (2, 98))
            data_stretched = np.clip(data, p2, p98)
            data_stretched = (data_stretched - p2) / (p98 - p2)
            
            # 转换为8位图
            data_8bit = (data_stretched * 255).astype(np.uint8)
            
            # 更新data为处理后的8位图
            data = data_8bit
            return [(data, {'name': 'FITS Image'}, 'image')]
    return None