# 06A：先验证单镜头外观转换

上轮上传的 `MiniMaxH3_Director_00007_.mp4` 出现灰模与正式装甲混杂、盾击特写延长、城市仍为灰模。内嵌执行参数显示 R2V、预演位于本段参考视频槽、源视频时间轴为空；Picture 1 为人物三视图，与提示词的城市来源不一致。Turbo 1.0 / 4 步配置正确，Combat 已旁路，共享提示词已关闭。模式差异不是已证实的唯一原因：R2V 与 RV2V 底层都使用参考视频条件，换模式不保证逐帧保留。

本测试只验证一位 Aegis 的**背面外观 → 四帧转身 → 右臂开盾**，不是新的成片打斗，也不替代背后突袭设计。镜头固定，人物占画面约一半高度，末尾保留举盾姿态以检查转换稳定性。没有怪兽、切镜和建筑爆破，减少同时需要转换的内容。

## 文件

- [single-shot-source-56f.mp4](single-shot-source-56f.mp4)：Blender 已渲染源视频，24 fps / 56 帧 / 2.333 秒，无声。
- [keyframes.jpg](keyframes.jpg)：带帧号的人工检查图。
- [workflow-rv2v-template.json](workflow-rv2v-template.json)：从上轮视频内嵌工作流整理的导入模板，已设 RV2V / 源视频时间轴模式，沿用现有模型文件名。未在用户 ComfyUI 实机运行验证。
- [prompt.txt](prompt.txt)：完整六字段提示词，模板已填好。
- [build_previs.py](build_previs.py)：Blender 4.3.2 生成脚本。

## 操作：只运行一次这个小测试

1. 下载工作流 JSON，用 ComfyUI 的“打开工作流”加载成新工作流。它不是 Director 的“导入导演包”格式。
2. 在 Director 的**源视频时间轴**上传 `single-shot-source-56f.mp4`。模板的视频路径故意留空，不能上传前直接运行。不要放到参考视频槽。
3. 确认时间轴出现实际源视频缩略图；只有一个完整 56 帧片段。模式显示 **rv2v — 参考素材改视频**。不要自动分镜。
4. 检查三个图片槽；若预填文件名不能加载，重新上传到对应槽位：

| 槽位 | 文件 | 唯一职责 |
|---|---|---|
| Picture 1 | 你现有的 `沈烈Aegis三视图_去背景-resize.png` | 同一位 Aegis 的前后装甲身份 |
| Picture 2 | [aegis-airborne-shield.png](../../references/states/aegis-airborne-shield.png) | 右前臂金色蜂窝盾的外观 |
| Picture 3 | [A-team.png](../../references/A-team.png) | 只参考背景城市材质与红月照明，不生成图内其他人物 |

这次重新编号为 1/2/3，不能沿用上次的 Picture 5。Picture 1 使用你现有原图，本包没有其本地副本。城市图单独放在 Picture 3，提示词已明确只取环境。

5. 模板已填入完整提示词。清除旧工作流的外部 Shared Params 连接或旧共享文本；本测试用本模板的全局完整提示词与三个参考槽，不额外叠加 EP3 的五角色定义。
6. 确认参数后生成：

| 参数 | 本轮 |
|---|---|
| UNET | `minimax_h3_ref2va_pruned_int8_convrot.safetensors` |
| Turbo LoRA | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors`，1.0 |
| Combat V2 | 已旁路；不加战斗触发词 |
| Steps / CFG | 4 / 1 |
| Sampler / Scheduler | euler / simple |
| Shift video / audio | 12 / 3 |
| Seed | 888 / fixed |
| 输出 | 864×480，24 fps，56 帧 |
| 段间引导 | 关闭 |
| 声音 | 静音 |

保留采样配置是为了减少本轮变化项，不代表已证明 Turbo 适合这个外观转换任务。无需先跑 25 步或叠加新 LoRA。

## 看哪里决定是否继续

| 源帧（零起始） | 动作 | 输出验收 |
|---|---|---|
| 0–19 | 背向悬停，盾未开 | 背甲、肩甲和头盔从第一帧就完成转换，不保留多面灰模 |
| 20–23 | 四帧完成 180° 转身 | 约 0.833–0.958 秒快速改变朝向，不新增切镜或慢转 |
| 22–23 | 盾展开 | 右前臂开盾，位置稳定；不把盾生成在另一只手上 |
| 24–55 | 举盾悬停 | 装甲持续一致，不变回灰模、不复制人物 |

背景应有完整 CG 材质，但第一优先级是角色身份与转身速度。此测试不检验撞击力道或击飞，不能仅凭它通过就认定整段战斗可行。

若此单镜头仍明显灰模化、身份跳变或转身被拉长，先停止扩大到四镜头。它说明当前输入与配置未通过基础转换验证；不据此断言 H3 所有配置都不行，也不继续承诺靠更长提示词能解决。

## 重建

```sh
blender -b -t 4 --python build_previs.py -- --output frames
ffmpeg -framerate 24 -i frames/%04d.png -frames:v 56 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart single-shot-source-56f.mp4
```

只完成 Blender 预演、导入模板和提示词；未运行 H3。提示词结构参考[官方 H3 skill](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/SKILL.md)，源视频接入方式参考 [Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director)。
