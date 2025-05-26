# 封包
python -m build

# API token
# 测试服
python -m twine upload --repository testpypi dist/* --verbose

# 删除本地打包文件
Remove-Item dist/*

# 安装测试包
pip install -i https://test.pypi.org/simple/ --upgrade mzcst-2024