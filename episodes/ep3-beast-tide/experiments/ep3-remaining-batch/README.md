# EP3 剩余镜头批量生成包

用户本机分别运行11个独立R2V工作流。此环境没有H3运行能力，视频尚未生成。镜头顺序如下；2秒UI对应56帧约2.333秒，11段源素材约25.67秒，精剪后时长依实际画面确定。

统一：Ref2VA int8；25 steps、CFG1、res_multistep/simple、shift12/3、seed888；Turbo和Motion Repair旁路。每个工作流独立加载组内参考图，按下表顺序上传。首轮可按编号全部排队，生成后检查动作和连贯性。数值与秒数为目标，非严格保证。

| 镜头 | 画面 | 参考图顺序 |
|---|---|---|
| 07C-approach | 接近巨兽 | 01-aegis-shield.png, 02-titan.png, 03-blade.png, 04-city.png |
| 07D-first-slash | 第一刀 | 01-aegis-shield.png, 02-titan.png, 03-blade.png |
| 07E-return-slash | 回身第二刀 | 01-aegis-shield.png, 02-titan.png, 03-blade.png, 08-damage.png |
| 07F-shield-evade | 化盾躲避 | 01-aegis-shield.png, 02-titan.png, 08-damage.png |
| 08A-tail-sweep | 巨尾扫击 | 01-aegis-shield.png, 02-titan.png, 07-tail.png |
| 08B-tail-impact-flight | 尾击高速击飞 | 01-aegis-shield.png, 02-titan.png, 07-tail.png, 04-city.png |
| 08C-ground-recovery | 落地恢复守护 | 01-aegis-shield.png, 05-team.png, 04-city.png |
| 09A-barrier-rise | 壁垒升起 | 01-aegis-shield.png, 05-team.png, 06-barrier.png |
| 09B-claw-pressure | 巨爪压罩 | 01-aegis-shield.png, 02-titan.png, 06-barrier.png |
| 10A-shield-fracture | 壁垒消散与盾裂 | 01-aegis-shield.png, 05-team.png, 06-barrier.png |
| 10B-red-eyes-finale | 红眼悬念 | 01-aegis-shield.png, 02-titan.png, 05-team.png, 04-city.png |

同一个右前臂刀盾转换；Aegis 1.88米，巨兽30米；两处刀伤形成于两次斩击，核心完整；末段才出现持续盾裂。击飞使用先前确认的瞬间光迹节奏。

R2V参考图指导外观，实际剪辑中的精确姿态、方位和人物尺度可能漂移；现有参考图部分为盾或组合图，持刀姿态及胸口伤痕尤其需审核。此包为可运行的生成准备，不是已生成视频。
