# 延迟一段时间
$delay = 5
Write-Output "暂停 $delay 秒，等待测试服更新"
# Start-Sleep -Seconds $delay
for ($i = 0; $i -lt $delay; $i ++) {
    $left = $delay - $i
    Write-Progress -Activity "等待 $delay 秒" -Status "还有 $left 秒" -PercentComplete ($i / $delay * 100)
    # Write-Output "还有 $left 秒"
    Start-Sleep -Seconds 1
    
}

# Write-Output "100% 进度条测试"
# for ($i = 1; $i -le 100; $i++ ) {
#     Write-Progress -Activity "Search in Progress" -Status "$i% Complete:" -PercentComplete $i
#     Start-Sleep -Milliseconds 1000
# }
Write-Output "end of 100% progress bar test"
