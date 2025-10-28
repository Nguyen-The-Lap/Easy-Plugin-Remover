# Easy FL Studio Plugin Manager

A user-friendly tool to manage and remove FL Studio plugins with a clean, intuitive interface.

> **Important:** This application requires administrator privileges to properly manage plugins. Please ensure you run it as Administrator.

**Author:** W1ll


## Features

- Scan for FL Studio plugins in common directories
- View detailed plugin information
- Safely remove unwanted plugins
- Clean and intuitive GUI
- Admin privileges handling
- No console windows shown during execution

## Requirements

- Windows 10/11
- Python 3.8+
- FL Studio (any version)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/easy-fl-plugin-manager.git
   cd easy-fl-plugin-manager
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from Source

1. Right-click on the application or command prompt
2. Select 'Run as administrator'
3. If using command line:
   ```bash
   # Windows
   runas /user:Administrator "python fl_plugin_remover.py"
   ```
   Or simply right-click and select 'Run as administrator' when using the executable.

### Building Executable

```bash
python build_exe.py
```

The executable will be created in the `dist` folder.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you find this tool useful, consider giving it a ⭐ on GitHub!
