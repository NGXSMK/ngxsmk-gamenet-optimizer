# Contributing to GameNet Optimizer

Thank you for your interest in contributing to GameNet Optimizer! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the [Issues](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/issues) page
- Provide detailed information about the problem
- Include system information and steps to reproduce
- Use appropriate labels (bug, enhancement, question)

### Suggesting Features
- Open a new issue with the "enhancement" label
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity

### Code Contributions
1. Fork the [repository](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer)
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Testing
- Test your changes thoroughly
- Add unit tests for new features
- Test on different operating systems if possible
- Verify backward compatibility

### Documentation
- Update README.md if adding new features
- Add docstrings to new functions
- Update comments for complex code
- Include usage examples

## 🛠️ Development Setup

### Prerequisites
- Python 3.7+
- Git
- Code editor (VS Code, PyCharm, etc.)

### Setup
1. Fork and clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run the application

```bash
git clone https://github.com/NGXSMK/ngxsmk-gamenet-optimizer.git
cd gamenet-optimizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python launcher.py
```

## 📁 Project Structure

```
gamenet-optimizer/
├── main.py                 # Main application entry point
├── launcher.py            # Application launcher
├── modules/               # Core optimization modules
│   ├── fps_boost.py      # FPS optimization
│   ├── network_analyzer.py # Network analysis
│   ├── multi_internet.py  # Multi-connection management
│   ├── traffic_shaper.py  # Traffic shaping
│   ├── ram_cleaner.py    # Memory optimization
│   ├── lol_optimizer.py  # League of Legends specific
│   └── config_manager.py # Configuration management
├── tests/                 # Test files
├── docs/                  # Documentation
└── examples/              # Usage examples
```

## 🎯 Areas for Contribution

### High Priority
- **Cross-platform support**: macOS compatibility
- **Additional games**: Support for more games
- **Network protocols**: Advanced networking features
- **Performance**: Code optimization and speed improvements

### Medium Priority
- **UI/UX**: Interface improvements
- **Documentation**: Better guides and examples
- **Testing**: More comprehensive test coverage
- **Localization**: Multi-language support

### Low Priority
- **Themes**: Customizable UI themes
- **Plugins**: Plugin system for extensions
- **Mobile**: Companion mobile app
- **Analytics**: Usage statistics (privacy-focused)

## 🐛 Bug Reports

When reporting bugs, please include:

1. **System Information**
   - Operating System and version
   - Python version
   - GameNet Optimizer version

2. **Bug Description**
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior

3. **Additional Information**
   - Screenshots if applicable
   - Error messages
   - Log files if available

## 💡 Feature Requests

When suggesting features:

1. **Clear Description**
   - What the feature should do
   - Why it would be useful
   - How it fits with existing features

2. **Use Cases**
   - Specific scenarios where it would help
   - Target audience
   - Potential impact

3. **Implementation Ideas**
   - Technical approach (if you have ideas)
   - Dependencies or requirements
   - Potential challenges

## 📝 Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### PR Description
- Clear title describing the changes
- Detailed description of what was changed
- Reference any related issues
- Include screenshots for UI changes
- List any breaking changes

### Review Process
- All PRs require review before merging
- Address feedback promptly
- Be open to suggestions and improvements
- Keep discussions constructive

## 🏷️ Labels and Milestones

### Issue Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested

### Milestones
- `v1.0`: Initial stable release
- `v1.1`: Minor improvements and fixes
- `v2.0`: Major feature additions

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **Issues**: For bug reports and feature requests
- **Wiki**: For detailed documentation
- **Email**: sachindilshan040@gmail.com
- **Maintainer**: @NGXSMK

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Community highlights

## 📄 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, trolling, or inflammatory comments
- Personal attacks or political discussions
- Public or private harassment
- Publishing private information without permission
- Other unprofessional conduct

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://conventionalcommits.org/)

---

Thank you for contributing to GameNet Optimizer! Together, we can make gaming optimization accessible to everyone.
