# 06B：俯视高速撞楼，承接已通过的撞盾镜头

上一段用户输出 `06A_rv2v_impact_separation_00001_.mp4` 已表现出约 0.2 秒的接触后快速出画。本镜从 Aegis **已经被击飞**开始，独立生成俯视撞楼与局部坍塌；生成完成后再剪辑衔接，不把多镜头重新塞入一个 H3 片段。

## 下载

- [overhead-building-source-56f.mp4](overhead-building-source-56f.mp4)：本轮唯一生成源；56 帧、24 fps、2.333 秒、无音轨。
- [cut-preview-H3-to-graybox.mp4](cut-preview-H3-to-graybox.mp4)：剪辑接点演示，**前段是用户上传的 H3 输出，后段是本轮灰模预演**。只看动作接点，不是最终 CG 成片，也不要上传它作为 H3 源视频。
- [workflow-rv2v-template.json](workflow-rv2v-template.json)：ComfyUI 模板，参数及完整提示词已填好。
- [prompt.txt](prompt.txt)：独立完整六字段提示词。
- [keyframes.jpg](keyframes.jpg)：标注源帧号，供人工检查。

## 用户环境操作

1. 用 ComfyUI 打开本目录工作流 JSON；不是 Director 的“导入导演包”格式。
2. 将 `overhead-building-source-56f.mp4` 上传到 **RV2V 源视频时间轴**。确认有实际缩略图，只有一个完整 56 帧片段，不自动分镜。
3. 参考图沿用上一轮四个槽：

| 槽位 | 文件 | 用途 |
|---|---|---|
| Picture 1 | 本机 `沈烈Aegis三视图_去背景-resize.png` | 装甲身份 |
| Picture 2 | [aegis-airborne-shield.png](../../references/states/aegis-airborne-shield.png) | 右臂盾外观 |
| Picture 3 | [A-team.png](../../references/A-team.png) | 城市材质和红月照明，不引入其他角色 |
| Picture 4 | 本机 `磐甲巨兽三视图_去背景-resize.png` | 巨兽外观 |

4. 保持 **Ref2VA、Turbo 1.0、4 steps、CFG 1、euler/simple、shift video/audio 12/3、seed 888 fixed、864×480**。Combat 旁路、段间引导关闭。不要额外连接旧 Shared Params 角色文本。
5. 保持静音；**CreateVideo 的 audio 输入留空**，Director 的 audio_vae 保留。模板已保留保存错误的修复。

没有为这一镜换模型、LoRA 或采样参数；它检验上轮有效配置能否应对远景比例和建筑破坏。

## 已渲染预演的时点

| 帧（零起始） | 时间 | 动作 |
|---|---|---|
| 0–3 | 0–0.167 秒 | 开场已经处于击飞中，向右高速穿过空隙；推进器关闭，盾跟随人物 |
| 4 | 0.167 秒 | 撞入目标楼第三层附近的外墙；接触后出现短冲击标记 |
| 5–7 | 0.208–0.333 秒 | 外墙破口形成，碎块散出；人物与盾进入建筑内部 |
| 8–55 | 0.333–2.333 秒 | 粉尘扩张、碎块落下，撞击层失稳，带动上部局部下沉并趋于稳定 |

巨兽 30 米，Aegis 1.88 米，塔楼约 40 米，高架约 12 米。远景人物很小，短白色拖尾帮助辨认，不把人物放大到巨人比例。建筑只在受击层附近失稳，上部下沉约一层，下部保留；是程序化运动示意，不是物理结构仿真。

## 与上一段怎样接

衔接演示使用用户上传上一段的**第 14–30 帧（包含两端）**，随后直接切到本镜源视频第 0 帧。即：保留短暂举盾、爪击和离开接触点，在人物尚未完全退出右边界时切俯视，继续保持向右运动。演示为 17 + 56 = 73 帧，24 fps，约 3.042 秒。

不保留上一段末尾长时间只有巨爪的空镜。不要以提示词里的时间直接剪辑 H3 成片：上一轮实际命中约第 28 帧，比其源视频提前四帧。本轮生成后也需要按实际命中和入墙帧微调接点。

上一段出画时脚部仍有亮焰，本镜目标是关闭喷射的被动飞行；切镜能改变可见细节，但不能保证消除这一连续性问题。正式合成需检查两个镜头的护盾外观、飞行方向、红月照明和街道布局。

## 验收与下一步条件

- 开场应继续快速位移，没有再次悬停、举盾或爪击。
- 人物在前几帧到达右侧建筑；白线不能变成独立导弹。
- 冲击闪光应发生在墙面接触位置，随后有破口、碎石和粉尘。
- 坍塌应保留可辨认的楼层变化，不能只用烟雾遮住原地不动的建筑。
- 巨兽与人物比例保持；人物入墙后不复制、瞬移返回或飞出恢复。

本轮只完成 Blender 源视频、剪辑接点演示、提示词和模板；未运行 H3，模板未在用户 ComfyUI 实机验证。若撞墙仍被拉长或建筑变化失败，记录该镜的具体失败，不因此重跑已通过的撞盾镜头。

## 重建

```sh
blender -b -t 4 --python build_previs.py -- --output frames
ffmpeg -framerate 24 -i frames/%04d.png -frames:v 56 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart overhead-building-source-56f.mp4
```
