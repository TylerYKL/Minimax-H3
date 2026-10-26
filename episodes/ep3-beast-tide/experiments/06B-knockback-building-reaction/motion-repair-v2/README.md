# Motion Repair V2：更新提示词与对照测试

承接击飞、撞楼、Nyx封闭面罩反应三段。原版完整保留在上级目录。本包使用相同六张首尾图，更新动作描述，并为击飞和撞楼加入Motion Repair V2单独使用的测试配置。

**模型文件不在包内。** 用户需要先将`Motion_Repair_V2.safetensors`放入本机`ComfyUI/models/loras/`。当前云环境下载被网络代理阻断；本包不代表模型已下载或安装。

## 先跑哪一份

| 文件 | Motion Repair | 用途 |
|---|---|---|
| 01-flight-baseline-workflow.json | 旁路 | 新提示词基准组 |
| 01-flight-workflow.json | 0.9 | 击飞对照测试 |
| 02-collision-baseline-workflow.json | 旁路 | 新提示词基准组 |
| 02-collision-workflow.json | 0.9 | 撞楼对照测试 |
| 03-nyx-workflow.json | 旁路 | Nyx面罩反应 |

优先测试01-flight两份，保持同一首尾图和种子。两份使用完全相同的新提示词，区别仅为Motion Repair节点旁路状态及输出文件名等元数据。旧提示词与新LoRA同时变化不能独立证明LoRA效果，因此提供这组对照。

两段动作提示词已加入作者提供的可选触发词`bunny_crisp_motion`。触发词不是安装或启用LoRA的替代；读取器必须实际加载权重。作者推荐单独使用约0.9，本次尚未实机验证此权重对当前FL2VA int8模型的兼容性与效果。检查控制台是否出现权重键不匹配或大量未加载信息。

[作者模型说明](https://huggingface.co/JOKER141/MiniMax-H3-General-Motion-Continuity-Repair)

## 参数与图槽

- 继续使用FL2VA、25steps、CFG1、res_multistep/simple、shift12/3、seed888、864×480、24fps，静音。
- Turbo节点旁路。原Combat节点在本实验副本中替换为Motion Repair节点，Combat没有参与加载。
- 三段界面请求秒数为1.3 /2 /1.3，预计输出39 /56 /39帧。
- 按编号上传`frames`中start/end图。图与前版相同，图槽仍须核对。
- 单组顺序运行。此包不提供将0.9权重统一套在Nyx段上的合并工作流。

## 提示词的主要改动

01明确“被击飞”而非主动飞行：胸口朝攻击者，背部带动身体向左，肩髋共同位移，脚部拖后，盾持续贴近前臂。用固定楼层格线衡量位移，尾段保持动势。

02明确因果顺序：背肩触墙→外墙向内破裂→身体进入房间→撞击闪光→局部支撑破坏→楼板倾斜和碎石下坠。限制为相邻楼层的局部损伤，以参考图保持空间关系。

03保留Nyx紫黑装甲与封闭面罩，通过短促转头、握枪收紧、身体前倾及红色警报灯表达担心。用户提供的Nyx脸部参考用于角色身份记录，本段保持面罩关闭。

TXT和JSON内的动作提示词均为正向描述，负向字段为空。Nyx损伤数字继续由后期HUD脚本添加，默认78%是可修改剧情测试值。

## 后期与验收

`add_hud.py`使用方式：

```sh
python add_hud.py Nyx-render.mp4 --output Nyx-hud.mp4 --damage 78
```

`Nyx-HUD-layout-preview.mp4`是静态参考图加HUD的布局演示，不是H3生成结果。

比较对照组中Aegis在同一帧的位置、身体结构、末段停留、撞击与破碎的先后顺序。即使连续性改善，最终快打节奏仍可通过剪辑实现：击飞约0.33秒、碰撞约1秒、Nyx反应约1.625秒。源片速度与最终剪辑速度分开评估。
