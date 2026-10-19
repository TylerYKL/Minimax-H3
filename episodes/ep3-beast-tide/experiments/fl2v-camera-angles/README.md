# EP3 多视角 FL2V 补充包

已生成 **四组、八张首尾帧**，附独立FL2V工作流和动作提示词。用于替换原十秒测试中的部分画面，不是追加一遍同样攻击。H3视频尚未渲染，模板未实机验证。

| 机位 | 首帧 | 尾帧 | 工作流 | 提示词 | 原始生成长度 | 建议剪辑用途 |
|---|---|---|---|---|---|---|
| A Aegis第一人称 | [图](frames/A-pov-start.png) | [图](frames/A-pov-end.png) | [JSON](A-pov-workflow.json) | [TXT](A-pov-prompt.txt) | 56帧 / 2.333秒 | 盾面接触与分离，约0.6–1秒 |
| B 怪兽肩后反打 | [图](frames/B-beast-ots-start.png) | [图](frames/B-beast-ots-end.png) | [JSON](B-beast-ots-workflow.json) | [TXT](B-beast-ots-prompt.txt) | 56帧 / 2.333秒 | 踏步挥刀、斩中，约0.7–1.2秒 |
| C 贴地侧拍 | [图](frames/C-ground-start.png) | [图](frames/C-ground-end.png) | [JSON](C-ground-workflow.json) | [TXT](C-ground-prompt.txt) | 56帧 / 2.333秒 | 撞路障和落地，约0.8–1.5秒 |
| D 高位俯拍 | [图](frames/D-overhead-start.png) | [图](frames/D-overhead-end.png) | [JSON](D-overhead-workflow.json) | [TXT](D-overhead-prompt.txt) | 39帧 / 1.625秒 | 落地后的位置交代，约0.4–0.8秒 |

## 运行

用ComfyUI打开对应JSON，向FL2V分组上传同一字母的start/end两图。确认图片缩略图；工作流文件名仅占位，不会自动上传图片。不要把第一人称首帧和侧面尾帧放在同一段，让模型猜中间绕镜。

沿用上个包的 **FL2VA、25 steps、CFG 1、res_multistep/simple、shift 12/3、seed 888 fixed、864×480、24fps**。Turbo和Combat旁路，段间引导关闭，静音导出；audio_vae仍连接。旧Ref2V LoRA名字可能仍在旁路节点显示，保持旁路即可。CLIP和VAE文件名若与本机不同，请选择已安装对应文件。

先测试A第一人称，再跑B/C；D是可选的短过渡。只传这组首尾图，不叠加团队合照或另一机位参考图。帧数遵守17k+5，原始长度不是最终剪辑占比。

## 剪辑方式

与[原十秒包](../fl2v-10s-combat/README.md)混剪：侧面扑进 → 第一人称接触 → 侧面分离 → 怪兽肩后挥刀 → 侧面击飞 → 贴地撞路障 → 俯拍交代落点 → 侧面追进举盾。

- 同一次攻击只表现一次完整动作。不同视角切在接触、挥刀或落地节点，不逐段从头到尾重放。
- A第一人称画面右侧的盾属于右臂，不要为匹配屏幕方向水平翻转。
- B尾帧实际呈现刀刃接触肩甲的节点，适合切到击飞；不要停留尾帧形成刀卡住的效果。
- C保留了较小的兽体；与其他机位的透视尺度尚有差异，需在动态素材中检查、选择切点。
- D是高位斜俯拍，画面无天际线，并非严格正交90度。首尾主体位移较小，只做短空间交代。
- 独立生成的不同机位未保证建筑位置达到三维场景级一致；每组内部保持相近构图，跨组通过动作剪辑衔接。

这些是机位素材，不保证模型执行精确分秒。最终十秒的取舍和变速应在收到H3视频后确定，不使用定格/慢放强行填满。八张图已检查机位和首尾对应，工作流已做静态结构检查。
