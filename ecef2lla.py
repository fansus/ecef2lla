import tkinter as tk
from tkinter import ttk
import math

def ecef_to_geodetic(x, y, z):
    # WGS84椭球参数（保持不变）
    a = 6378137.0
    f = 1/298.257223563
    b = a * (1 - f)
    e = math.sqrt(a**2 - b**2) / a

    longitude = math.atan2(y, x)
    p = math.sqrt(x**2 + y**2)
    phi = math.atan2(z, p * (1 - e**2))

    for _ in range(10):
        N = a / math.sqrt(1 - e**2 * math.sin(phi)**2)
        h = p / math.cos(phi) - N
        phi_new = math.atan2(z, p * (1 - e**2 * N / (N + h)))
        if abs(phi_new - phi) < 1e-15:
            break
        phi = phi_new

    N = a / math.sqrt(1 - e**2 * math.sin(phi)**2)
    h = p / math.cos(phi) - N

    return (math.degrees(phi), math.degrees(longitude), h)

def copy_to_clipboard():
    result_text = result_textbox.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(result_text)
    root.update()  # 保持剪贴板内容

def convert():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
    except ValueError:
        result_textbox.config(state=tk.NORMAL)
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "错误：请输入有效的数字")
        result_textbox.config(state=tk.DISABLED)
        return
    
    try:
        lat, lon, alt = ecef_to_geodetic(x, y, z)
        result_str = f"纬度: {lat:.8f}°\n经度: {lon:.8f}°\n高度: {alt:.3f}米"
        result_textbox.config(state=tk.NORMAL)
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, result_str)
        result_textbox.config(state=tk.DISABLED)
    except Exception as e:
        result_textbox.config(state=tk.NORMAL)
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, f"转换错误：{str(e)}")
        result_textbox.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("ECEF坐标系转换工具 V2.0")
root.resizable(False, False)

# 输入框框架
input_frame = ttk.Frame(root, padding=10)
input_frame.pack()

# 输入组件布局（保持不变）
ttk.Label(input_frame, text="X坐标:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_x = ttk.Entry(input_frame, width=25)
entry_x.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Y坐标:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_y = ttk.Entry(input_frame, width=25)
entry_y.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Z坐标:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_z = ttk.Entry(input_frame, width=25)
entry_z.grid(row=2, column=1, padx=5, pady=5)

# 转换按钮
convert_btn = ttk.Button(input_frame, text="转换", command=convert)
convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

# 结果显示区域（改为Text组件）
result_textbox = tk.Text(input_frame, 
                        height=4, 
                        width=35,
                        font=('TkDefaultFont', 9),
                        padx=5,
                        pady=5,
                        wrap=tk.WORD,
                        state=tk.DISABLED)
result_textbox.grid(row=4, column=0, columnspan=2)

# 复制按钮
copy_btn = ttk.Button(input_frame, text="复制结果", command=copy_to_clipboard)
copy_btn.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()