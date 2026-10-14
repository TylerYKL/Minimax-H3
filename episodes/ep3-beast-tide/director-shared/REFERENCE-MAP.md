# EP3 新参考图分配（2026-10-14）

采用 r2v / Ref2VA。Shared Params 开启，放 common-prompt.txt；各 Group 只贴 groups/ 内对应文本。完整 prompts/ 为关闭 Shared Params 时使用，编号与本表一致。JSON 是手动配置清单，不是可直接导入的工作流。

## 固定 Shared 图片

|编号|文件|用途|
|---|---|---|
|Picture 1|references/A-team.png|Aegis 基础外观、战场氛围；Nyx/Lyra 以新图为准|
|Picture 2|references/states/titan-scale-preview.png|巨兽外观；比例仍待校准，不能作为精确比例图|
|Picture 3|references/states/nyx-aim.png|Nyx 外观与炮体结构|
|Picture 4|references/states/lyra-skill.png|Lyra 外观与双腕环技能|

## 各 Group 追加图片

以下文件名在 references/ 或 references/states/ 下；精确路径见 manifest.json。槽位从 Picture 5 开始，不覆盖共享图片。

|段|目标时长|本段追加|
|---|---|---|
|01|6s||
|02|4s||
|03|6s|Picture 5: C-blade-contact；Picture 6: nyx-fire|
|04|4s|Picture 5: lyra-repair|
|05|8s||
|06|8s|Picture 5: C-blade-contact|
|07|7s|Picture 5: C-blade-contact；Picture 6: titan-wounded|
|08|6s|Picture 5: titan-tail-contact；Picture 6: titan-wounded|
|09|4s|Picture 5: titan-tail-contact；Picture 6: titan-wounded|
|10|6s|Picture 5: titan-dome-pressure|
|11|6s|Picture 5: titan-dome-pressure；Picture 6: titan-wounded|
|12|10s|Picture 5: F-shield-fracture；Picture 6: titan-dome-pressure；Picture 7: titan-wounded|

## 使用限制与测试

- 八张新增图均已打包，使用最终修正版；原始角色三视图及 Aegis 三状态图文件尚未在工作区找到，未宣称打包。
- 比例图和动作图仍未准确体现16:1；文字约束不能保证修复图片偏差。先做第06段短片测试，检查30米巨兽和1.88米Aegis在同一景深的尺度。正式批量渲染前仍需校准比例参考。
- 受伤图只参考岩甲剥落材质，图中伤口布局与压罩图不完全一致。统一以第07段结束时的两道刀伤为后续状态，红色核心完整。
- 第01–04段不显示巨兽；第05–06段胸甲未受刀伤；第07段依次产生两道刀伤；第08–12段保留；护罩及盾牌的持久裂纹留到第12段。
- 新图片是外观/动作参考，不是固定首帧。灰底不进入影片，参考中的其他人物也不自动进入当前镜头。
- 先测06，再测07和08；确认右臂刀盾切换、尾根位置、接触后受力及镜头轴线。多机位保持06/07/08/11原来的三个镜头，不增加切镜负担。
- 保留你已验证的4-step Turbo LoRA配置；本次没有验证采样器、CFG、LoRA强度，也没有实际渲染视频。
