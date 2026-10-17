# 06A：盾已展开，命中后立即分离

上轮 `06A_rv2v_single_shot_00002_.mp4` 的装甲替换和短促转向已明显改善，但盾展开仍被拉长。本轮不再同时测试开盾：开头盾已完整展开，只验证**巨爪撞盾后，Aegis 能否立即与爪子分离并高速出画**。

这是独立的动作保留测试，开头与结尾留有检查余量，不是最终 EP3 剪辑节奏。没有背后察觉、转身、俯视切镜或撞楼；原来的完整战斗设计保留。

## 下载并运行

- [预演／源视频：impact-separation-source-56f.mp4](impact-separation-source-56f.mp4)
- [ComfyUI 工作流模板](workflow-rv2v-template.json)
- [完整提示词](prompt.txt)
- [关键帧](keyframes.jpg)

1. 在 ComfyUI 打开模板 JSON（不是 Director 的“导入导演包”格式）。
2. 在 Director 的**源视频时间轴**上传本目录 `impact-separation-source-56f.mp4`，确认实际缩略图和一个 56 帧片段。不要沿用上轮转身视频，也不要放入参考视频槽。
3. 模式应为 **rv2v — 参考素材改视频**，共 56 帧／24 fps／约 2.33 秒。上传后检查没有自动拆段。
4. 检查以下参考图槽。模板预填了你使用过的文件名，如果加载失败，上传到相同编号：

| 槽位 | 素材 | 用途 |
|---|---|---|
| Picture 1 | 现有 `沈烈Aegis三视图_去背景-resize.png` | Aegis 装甲身份 |
| Picture 2 | [aegis-airborne-shield.png](../../references/states/aegis-airborne-shield.png) | 右前臂盾外观 |
| Picture 3 | [A-team.png](../../references/A-team.png) | 只取背景城市材质、光照 |
| Picture 4 | 现有 `磐甲巨兽三视图_去背景-resize.png` | 巨爪与前臂岩甲外观 |

两张三视图沿用你本机原图，本包没有原图本地副本。Picture 4 本轮是巨兽，不是旧 EP3 的 Lyra 槽位。不要叠加旧 Shared Params 角色定义。

5. 模板已填完整全局提示词；保持 **Ref2VA、Turbo 1.0、4 steps、CFG 1、euler/simple、shift video/audio 12/3、seed 888 fixed、864×480**。Combat 保持旁路，段间引导关闭。
6. 保持静音。**CreateVideo 的 audio 输入不接线**，images/fps 正常连接；Director 的 audio_vae 必须保留。此设置继承上一轮 SaveVideo 音频编码报错的修复。

## 源视频的实际时点

帧号从零开始；这里描述已渲染的预演，H3 仍可能改变时间与轨迹。

| 帧 | 时间 | 内容 |
|---|---|---|
| 0–27 | 0–1.167 秒 | 固定镜头，完整盾已展开，Aegis 悬停，脚底喷射 |
| 28–31 | 1.167–1.333 秒 | 巨爪从左侧快速进入并接近 |
| 32 | 1.333 秒 | 爪击盾面，短白色冲击标记，脚底喷射关闭 |
| 33 | 1.375 秒 | 下一帧已有明显间隙，Aegis 带盾后移；冲击波展开 |
| 34–36 | 1.417–1.500 秒 | Aegis 加速穿过右边界，细白位移线辅助观察 |
| 37–55 | 1.542–2.333 秒 | 人物已出画，巨爪完成短暂随动和回收；镜头保持固定 |

人物始终 1.88 米；巨爪沿用 30 米巨兽的局部比例。灰模、白色冲击块、圆环和轨迹线都是外观转换的引导，不是最终光效。

## 本轮只用这三个问题验收

- 命中后下一帧是否开始离开爪子，而不是维持推盾姿势？
- 从接触到出画是否约 0.17 秒以内，而不是匀速慢飘？
- 盾是否跟随同一个 Aegis 离开，接触点有没有留下第二个人或一面悬空盾？

先核对接触和分离，再检查装甲、爪子、冲击光效。如果单镜头通过，再制作独立俯视击飞／撞楼镜头；暂不恢复四镜头一起生成。即使此轮通过，也只说明这个局部输入在该配置下有效。

Blender 源视频已渲染和逐帧检查；H3 转换尚未运行。工作流模板已做 JSON、图连接与参数检查，未在用户 ComfyUI 实机验证。

## 重建

```sh
blender -b -t 4 --python build_previs.py -- --output frames
ffmpeg -framerate 24 -i frames/%04d.png -frames:v 56 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart impact-separation-source-56f.mp4
```
