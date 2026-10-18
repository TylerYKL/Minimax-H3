# EP3 每段十秒：先生成第 01、02 段

按用户要求，把 EP3 另编成 **8 段 × 10 秒 = 80 秒**的剪辑方案。本轮只完成前两段灰模，分别对应原稿 00–10 秒“兽潮压境”和 10–20 秒“双线分工”。原 75 秒剧情文件不覆盖；后六段仍是规划，不是已生成素材。

## 下载与观看

| 内容 | 严格十秒预览 | H3 输入源视频 | 工作流 | 完整提示词 |
|---|---|---|---|---|
| 01 兽潮压境 | [观看](exports/EP3-01-preview-10s.mp4) | [243 帧源视频](exports/EP3-01-H3-source-243f.mp4) | [JSON](exports/EP3-01-workflow.json) | [TXT](exports/EP3-01-prompt.txt) |
| 02 双线分工 | [观看](exports/EP3-02-preview-10s.mp4) | [243 帧源视频](exports/EP3-02-H3-source-243f.mp4) | [JSON](exports/EP3-02-workflow.json) | [TXT](exports/EP3-02-prompt.txt) |

[连续观看前 20 秒](exports/EP3-first-20s-preview.mp4) · [第 01 段关键帧](exports/EP3-01-keyframes.jpg) · [第 02 段关键帧](exports/EP3-02-keyframes.jpg)

角色以颜色区分：黑灰橙金=Aegis，紫色=Nyx，青绿=Lyra，蓝灰=伤员；小兽为灰色四足、红眼。它们是简易动画代理，不是最终角色模型。两段共用场景、角色和世界时间，位置及损伤在段间延续。

## 为什么给两个时长版本

- 预览：**240 帧／24 fps，严格 10.000 秒**。
- H3 源：**243 帧／24 fps，10.125 秒**。已检查的 Director 帧数对齐代码使用 `17k+5`，240 会向上对齐到 243。
- 多出的三帧是末尾继续运动的余量，不是放慢整段。H3 输出在确认主要动作没有延后以后，裁取前 240 帧得到十秒；不要改 fps 或整体加速来凑时长。
- 第 01 段余量保持该段最后一个镜头，避免额外三帧引入下一段的切镜；第 02 段的起始状态仍按世界第 10 秒独立计算。

## 在你的 H3 Director 里测试

1. 用 ComfyUI 打开对应 `EP3-01-workflow.json` 或 `EP3-02-workflow.json`，不要用“导入导演包”。
2. 将对应的 **H3-source-243f.mp4** 上传到 **RV2V 源视频时间轴**。看到实际缩略图后，确认只有一个覆盖全段的 243 帧片段，不自动分镜。
3. 检查六个参考槽，两个段落使用相同编号：

| 槽位 | 素材 | 用途 |
|---|---|---|
| Picture 1 | 你本机 `沈烈Aegis三视图_去背景-resize.png` | Aegis 身份，多个方向只表示一个人 |
| Picture 2 | [nyx-aim.png](../../references/states/nyx-aim.png) | Nyx 与长炮 |
| Picture 3 | [lyra-skill.png](../../references/states/lyra-skill.png) | Lyra 兜帽装甲与腕部能量 |
| Picture 4 | [A-team.png](../../references/A-team.png) | 城市环境与光照 |
| Picture 5 | [aegis-airborne-shield.png](../../references/states/aegis-airborne-shield.png) | 右臂盾设计，不照搬悬停姿势 |
| Picture 6 | [C-blade-contact.png](../../references/C-blade-contact.png) | 只取能量刀外观，不引入图内巨兽 |

本轮编号不同于最近撞楼测试的四槽方案。提示词已配套重写；不要叠加旧 Shared Params 角色定义。这前二十秒只有小兽，没有三十米巨兽登场。小兽目前没有单独身份参考图，其形态来自源视频及文字定义。

4. 模板保留已测试参数：Ref2VA、Turbo 1.0、4 steps、CFG 1、euler/simple、shift video/audio 12/3、seed 888 fixed、864×480、24 fps。Combat 旁路，段间引导关闭。
5. 继续静音导出，CreateVideo 的 audio 输入留空；Director 的 audio_vae 保留。原稿台词和声音未在灰模中制作，本轮先验证画面。

这次遵照用户要求按十秒整段输入，**没有把每个镜头再拆成独立 H3 任务**。每段含五个机位；此前只验证过较短单镜头，十秒多镜头的时序与身份保留尚未实测。不保证源视频里的每个切点在生成后原样保留。

## 前两段镜头安排

### 01｜世界 00–10 秒

| 段内时间 | 内容 |
|---|---|
| 0–2 秒 | 街道与防线建立，兽群从北方逼近 |
| 2–4 秒 | 低位跟拍小兽奔跑 |
| 4–6.5 秒 | 三人守线，Aegis 右臂盾展开 |
| 6.5–8.5 秒 | 第一只小兽撞盾，Aegis 受压滑退，小兽反弹 |
| 8.5–10 秒 | Nyx 移向西侧平台，Lyra 转向后方伤员 |

### 02｜世界 10–20 秒

| 段内时间 | 内容 |
|---|---|
| 0–2.4 秒 | Nyx 高台点射，目标小兽受击 |
| 2.4–5 秒 | Aegis 收盾出刀，一次快速斜斩击退漏网小兽 |
| 5–7.5 秒 | Lyra 腕部修复伤员肩甲，后线开始向南撤 |
| 7.5–8.7 秒 | 水洼波纹、碎石震动 |
| 8.7–10 秒 | 兽群向两侧让路，中央通道打开，留下巨兽现身伏笔 |

## 整集十秒分段草案

| 段 | 时间 | 内容 | 本轮状态 |
|---|---|---|---|
| 01 | 00–10 | 兽潮压境 | 灰模已生成 |
| 02 | 10–20 | 双线分工 | 灰模已生成 |
| 03 | 20–30 | 巨兽破潮、尺度揭示、起飞 | 仅规划 |
| 04 | 30–40 | 背后突袭、盾击、击飞撞楼 | 仅规划 |
| 05 | 40–50 | 脱出废墟、绕肩双斩 | 仅规划 |
| 06 | 50–60 | 巨尾反扑、坠地制动、守线 | 仅规划 |
| 07 | 60–70 | 不动壁垒、巨爪压罩、撤离 | 仅规划 |
| 08 | 70–80 | 领域消散、盾裂、红眼悬念 | 仅规划 |

这是针对已认可的撞楼方向调整后的 80 秒剪辑草案，后续仍需检查伤势、桥体损坏与原稿衔接。[机器可读方案](episode-plan.json)

## 重建

```sh
blender -b -t 4 --python render.py -- --segment 1 --output /path/frames/01
blender -b -t 4 --python render.py -- --segment 2 --output /path/frames/02
python export.py --frames /path/frames
```

Blender 4.3.2 / Python 3 / ffmpeg。`export.py` 复用仓库内已有 RV2V 模板，因此保留仓库目录结构。前排遮挡楼体在预演中隐藏以保持动作可读性；没有采用真实城市破坏模拟。小兽以简化跑步周期和明确接触轨迹表现，角色尚未使用正式骨骼动作库。

已检查预览帧数、时长、参考编号、工作流连接和源动画关键画面；未在用户 GPU 上运行 H3。
