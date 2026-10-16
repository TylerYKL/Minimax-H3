# 06A 背后突袭：修订动作预演

按最新要求改成：**巨爪突然出现在背后 → 寒意反应闪过 → Aegis 快速转身开盾 → 两帧冲击 → 极速击飞撞楼**。删除上一版的慢速逼近。这里是 Blender 三维灰模动作预演，尚未经过 H3 外观转换；角色细节、光效和建筑破坏均为示意。

## 先看与下载

- [两秒预览](06A-rear-ambush-preview-2s.mp4)：48 帧，检查突袭、转身和击飞节奏。
- [H3 源视频](06A-rear-ambush-source-56f.mp4)：56 帧，24 fps，约 2.33 秒。末尾八帧继续坍塌，供转换与剪辑使用。
- [关键帧](keyframes.jpg)：带帧号的人工检查图，不作为模型参考图上传。
- [完整 RV2V 提示词](rv2v-complete.txt)：六字段独立版本。
- [Blender 制作脚本](build_previs.py)：可重复渲染；没有使用用户上传的视频进行加速拼接。

## 节奏与镜头

帧号从零开始，按 24 fps 计算。表格时间是预演实际动作，不代表 H3 能严格按文字逐帧执行。

| 帧 | 时间范围 | 画面 |
|---|---|---|
| 0–4 | 0.000–0.208 秒 | 侧面镜头：Aegis 朝右悬停，背对来袭方向，脚底持续喷射 |
| 5–7 | 0.208–0.333 秒 | 巨爪从左后方突然闯入，继续逼近；无慢镜 |
| 8–10 | 0.333–0.458 秒 | 切背部近景，肩膀微耸，冷色闪光掠过背甲，表现背后一凉 |
| 11–14 | 0.458–0.625 秒 | 切回侧面，四帧转身；第 13 帧开始开盾，第 14 帧完全展开 |
| 15–16 | 0.625–0.708 秒 | 爪击盾面，白金冲击标记、扩张波环；喷射关闭，人物立刻后移分离 |
| 17–20 | 0.708–0.875 秒 | 硬切高位俯视，四帧跨越间隔，细白轨迹标示高速击飞 |
| 21–47 | 0.875–2.000 秒 | 撞入外墙，冲击闪光、碎块散出，上方楼层开始下沉 |
| 48–55 | 2.000–2.333 秒 | 坍塌继续；人物留在破口内部 |

背部蓝线只标示“寒意闪过”的位置，不是新增装备或背盾。冲击白球和扩张圆环是特效位置标记，转换后应成为短闪光与折射冲击波。坍塌由程序轨迹驱动，不是结构力学模拟。视频无字幕、无水印、无音轨。

Aegis 高 1.88 米，巨兽角尖离地 30 米，塔楼约 40 米，高架约 12 米。俯视下人物很小是正确比例，靠短白轨迹辨认。右臂开盾，本镜不出刀。

## MiniMax H3 Director 测试

1. 复制测试工作流，选择 **rv2v — 参考素材改视频**，使用 Ref2VA 模型。
2. 把 **56 帧源视频** 放进源视频时间轴，作为一个完整片段，不要自动拆成四个独立生成段，也不要仅放在 R2V 参考视频槽。它对应 `<Video 1>`。
3. 关闭段间引导和引用上段，移除旧踢击视频。完整提示词替换为本目录的 `rv2v-complete.txt`，不要再叠加旧 Shared/Common Prompt。
4. 参考图继续使用原槽位：
   - Picture 1：`../../references/A-team.png`，Aegis 造型与城市外观。
   - Picture 2：`../../references/states/titan-scale-preview.png`，巨兽外观；人物比例以源视频为准。
   - Picture 5：`../../references/states/aegis-airborne-shield.png`，右前臂盾设计。保留编号 5，不改成 3。
5. 首轮沿用现有 Turbo 1.0、4 steps、euler/simple、CFG 1、seed 888、video/audio shift 12/3；旁路 Combat V2，不加 `prfight2` / `prfin1`。这一轮检验源动作保留，配置仅为实验起点。
6. 输出 24 fps、56 帧；分辨率可保持现有 864×480。源视频 960×540 不要求输出也采用 540 高度。声音选择生成或静音，源文件没有原声。

RV2V 不是严格骨骼重定向，仍可能改变动作时序、镜头或比例。这一版只完成预演与提示词，没有在用户环境运行 H3。先检查灰模速度，再判断转换是否保留：如果预演快、H3 输出慢，问题发生在转换阶段。

验收重点：巨爪是否从背后突然出现、寒意镜头是否一闪即过、转身是否先于盾面接触、接触是否仅两帧、切俯视后是否四帧到墙边。最后再检查外观；不要为追求装甲细节接受重新变慢的动作。

此版本结尾人物进入建筑，不能直接接回旧 06B 的空中翻滚开头。旧实验与正式 EP3 文件保持原状。

## 重建

```sh
blender -b -t 4 --python build_previs.py -- --output frames
ffmpeg -framerate 24 -i frames/%04d.png -frames:v 56 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart 06A-rear-ambush-source-56f.mp4
ffmpeg -i 06A-rear-ambush-source-56f.mp4 -frames:v 48 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart 06A-rear-ambush-preview-2s.mp4
```

提示词结构沿用 [官方 h3-prompt-writing](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/SKILL.md)；模式说明见 [MiniMax H3 Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director)。`manifest.json` 是本实验记录，不是可导入工作流。
