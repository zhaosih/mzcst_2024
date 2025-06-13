# 封包
python -m build

# API token
# 测试服
Write-Output "上传到测试服"
python -m twine upload --repository testpypi dist/* --verbose

# 删除本地打包文件
Write-Output "删除本地打包文件"
Remove-Item dist/*

# 延迟一段时间
$delay = 60
$interval = 10
Write-Output "暂停 $delay 秒，等待测试服更新"
# Start-Sleep -Seconds $delay
for ($i = $delay; $i -gt 0; $i = $i - $interval) {
    Write-Output "还有 $i 秒"
    Start-Sleep -Seconds $interval
}

# 更新测试包
Write-Output "更新测试包"
pip install -i https://test.pypi.org/simple/ --upgrade mzcst-2024