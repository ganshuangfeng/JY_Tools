
TODO:
  源码 切换分支、更新
  服务器 停机； 备份日志；备份旧文件；
  切换、回滚版本：部署失败可以快速回滚（用 python 处理元数据）

★ 重启后可能要做的事

  1、节点，启动 nfs 服务
    service nfs-kernel-server start

  2、中心，挂载各节点的文件系统
    转到文件夹 /home/jyserver/deploy_center/nodes
    执行挂载命令：
    mount -t nfs 172.18.107.235:/home/deploy/nodes ./data
    mount -t nfs 172.18.107.233:/home/deploy/nodes ./game
    mount -t nfs 172.18.107.234:/home/deploy/nodes ./gate



