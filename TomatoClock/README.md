# 🍅 超级番茄钟 (Enhanced Tomato Clock)

一个优雅、高效的番茄工作法计时器，专为提高工作专注度而设计。

## ✨ 功能特性

### 🎯 核心功能
- **经典番茄工作法**: 25分钟工作 + 5分钟短休息 + 15分钟长休息
- **智能循环**: 每4个番茄后自动进入长休息
- **悬浮窗设计**: 始终置顶，不干扰工作
- **一键操作**: 支持键盘快捷键和鼠标操作

### 🎨 用户界面
- **现代化设计**: 深色主题，护眼美观
- **透明效果**: 半透明窗口，与桌面融合
- **紧凑型**: 120x100像素，最小化屏幕占用
- **可拖动**: 任意位置摆放，自动保存位置

### ⌨️ 快捷键
| 快捷键 | 功能 |
|--------|------|
| `空格键` | 暂停/继续 |
| `R` | 重置计时器 |
| `S` | 跳过当前阶段 |
| `N` | 进入下一阶段 |
| `C` | 打开设置 |
| `Q` | 退出程序 |

### ⚙️ 自定义配置
- 工作时长自定义
- 短休息/长休息时长设置
- 长休息间隔配置
- 窗口位置记忆
- 透明度调节

## 🚀 快速开始

### 方法一：直接运行
```bash
# 克隆项目
git clone https://github.com/your-username/tomato-clock.git
cd tomato-clock

# 运行程序
python enhanced_tomato_clock.py
```

### 方法二：打包为可执行文件
```bash
# 安装打包工具
pip install pyinstaller

# 打包为Windows可执行文件
pyinstaller --onefile --windowed --icon=tomato.ico enhanced_tomato_clock.py

# 打包文件在 dist/ 目录
```

### 方法三：创建快捷方式
1. 右键点击 `enhanced_tomato_clock.py`
2. 选择"发送到" → "桌面快捷方式"
3. 双击快捷方式即可运行

## 📁 项目结构

```
tomato-clock/
├── 📄 enhanced_tomato_clock.py    # 主程序文件
├── 📄 tomato_clock.py            # 简单版本（兼容旧版）
├── 📄 README.md                  # 项目说明
├── 📄 requirements.txt           # 依赖列表
├── 📄 .gitignore                # Git忽略文件
├── 📁 docs/                     # 文档目录
├── 📁 screenshots/              # 截图目录
├── 📁 tests/                    # 测试文件
└── 📁 C++/                      # Visual Studio C++版本
    ├── TomatoClock.sln
    └── TomatoClock/
```

## 🎯 使用方法

1. **启动程序**: 双击运行后，会在屏幕右上角出现一个小窗口
2. **开始工作**: 默认25分钟倒计时开始
3. **休息提醒**: 时间到后会自动蜂鸣并进入休息时间
4. **调整设置**: 按 `C` 键或双击窗口打开设置面板
5. **位置调整**: 鼠标拖动窗口到任意位置

## ⚙️ 配置说明

配置文件保存在用户目录下：
- **Windows**: `C:\Users\用户名\.tomato_config.json`
- **Linux/Mac**: `~/.tomato_config.json`

### 配置选项
```json
{
  "work_time": 25,                    // 工作时长(分钟)
  "short_break": 5,                   // 短休息时长(分钟)
  "long_break": 15,                   // 长休息时长(分钟)
  "sessions_before_long_break": 4,    // 长休息间隔(番茄数)
  "window_x": 100,                    // 窗口X坐标
  "window_y": 50,                     // 窗口Y坐标
  "always_on_top": true               // 是否置顶
}
```

## 🖥️ 系统要求

- **操作系统**: Windows 7/8/10/11, macOS, Linux
- **Python版本**: 3.6 或更高
- **依赖**: 仅使用Python标准库，零依赖

## 📸 截图展示

### 主界面
![主界面](./screenshots/main_window.png)

### 设置面板
![设置面板](./screenshots/settings.png)

### 右键菜单
![右键菜单](./screenshots/context_menu.png)

## 🛠️ 开发

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 依赖安装
pip install -r requirements.txt
```

### 代码规范
- 遵循PEP 8代码规范
- 使用有意义的变量名和函数名
- 添加必要的注释和文档字符串

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 贡献步骤
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 番茄工作法由 [Francesco Cirillo](https://francescocirillo.com/) 创建
- 感谢所有贡献者和用户的支持

## 📞 联系方式

- **项目地址**: [GitHub](https://github.com/your-username/tomato-clock)
- **问题反馈**: [Issues](https://github.com/your-username/tomato-clock/issues)
- **邮箱**: your-email@example.com

---

**享受高效工作，从番茄钟开始！** 🍅✨