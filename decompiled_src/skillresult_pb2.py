#Embedded file name: /WORKSPACE/data/entities/common/proto/skillresult_pb2.o
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='skillresult.proto', package='skillresult', serialized_pb="\nskillresult.protoskillresult\"W\n	MoveParam\r\nrefId (\r\nsrcPos (B\ndistFixType (\n\ndistFixVal (\">\n\rSpecialEffect\nseid (\r\nseType (\r\nseValue (\r\">\nDmgAbsorbValue\r\nvalue (\nsource (\r\r\nsrcid (\r\":\n	DmgAbsorb-\nelements (2.skillresult.DmgAbsorbValue\"�\nResult\r\nsrcid (\r,\n	dmgSource (2.skillresult.DAMAGESOURCE\ndmgSourceId (\r\ndmgs (B\nhps (\nmps (\neps ()\n	dmgAbsorb (2.skillresult.DmgAbsorb%\nars	 (2.skillresult.DAMAGEPOWER\nseId\n (\r\nlabours (\ncomboNum (\r\ncomboDmg\r (\r*\n\nhealAbsorb (2.skillresult.DmgAbsorb\"F\nControllStateData\ncontrollStateId (\r\ncontrollStateHit (\"w\n\nFenshenVal\n\nid (\r)\n\nfenshenPos (2.skillresult.Position%\ntgtPos (2.skillresult.Position\nyaw (\"�\n	ResultSet\neid (\r$\nresults (2.skillresult.Result\nmoveId (\r\nmoveTime ()\n	moveParam (2.skillresult.MoveParam\nkill (\nrealDmg (9\ncontrollStateData (2.skillresult.ControllStateData0\n\raddFlagStates	 (2.skillresult.FlagStateVal\ndispellFlagStates\n (\r(\nfenshen (2.skillresult.FenshenVal\"+\nPosition	\nx (	\ny (	\nz (\"5\nFlagStateVal\nflagStateId (\r\nlastTime (\"�\nSkillResult\r\ntgtId (\r\nnum (\r\n\nlv (\r\'\nresults (2.skillresult.ResultSet\nisInstantSkill (\npos (B\ndontPlayAction (\n\rguideCastTime (\n\ncd	 (\ngcd\n (\n	timeStamp (\"[\nPSkillResult\npskillId (\r\npskillLv (\r\'\nresults (2.skillresult.ResultSet\"�\nAttackResult\r\ntgtId (\r\'\nresults (2.skillresult.ResultSet\n\nresultType (\r\ndontPlayAction (\nnextAtkDelay (\"�\nMFResult\nmagicfieldId (\r\nnum (\r\n\nlv (\r\'\nresults (2.skillresult.ResultSet\nskillId (\r\nskillLv (\r\'\nrPosList (2.skillresult.Position\"m\n\rFenshenResult\n	fenshenId (\r\'\nresults (2.skillresult.ResultSet\nskillId (\r\nskillLv (\r\"t\nGuideSkillResult\r\ntgtId (\r\nnum (\r\n\nlv (\r\'\nresults (2.skillresult.ResultSet\npos (B\"(\nCombatMessageArg	\nd (	\ns (\"�\n\rCombatMessage\nnum (\r+\nargs (2.skillresult.CombatMessageArg\ndmg0 (\r\ndmg1 (\r\ndmg2 (\r\ndmg3 (\r\ndmg4 (\r\ndmg5 (\r\ndmg6	 (\r\ndmg7\n (\r\ndmg (\r\ntoall (\":\nStateResult+\ndetails (2.skillresult.StateMessages\"�\n\rStateMessages\nstateId (\r\nstateSrc (\nstateTgt (\r\r\naddHp (\r\nreduceHp (\r\r\naddMp (\r\nreduceMp (\r*5\nDM\n\nDM_ADD \n\nDM_SUB\nDM_NONE\n\nDM_CRI*�\nDAMAGEPOWER\r\n	DP_NORMAL \nDP_CRIT\nDP_AVOID\nDP_ACCURACY\nDP_BLOCK\nDP_SLIP\nDP_WUDI\n\nDP_HP_CRIT\n*9\nDAMAGESOURCE\nDM_SKILL_EFFECT \nDM_SKILL_REFLECT")
_DM = _descriptor.EnumDescriptor(name='DM', full_name='skillresult.DM', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='DM_ADD', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DM_SUB', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DM_NONE', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DM_CRI', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=2619, serialized_end=2672)
DM = enum_type_wrapper.EnumTypeWrapper(_DM)
_DAMAGEPOWER = _descriptor.EnumDescriptor(name='DAMAGEPOWER', full_name='skillresult.DAMAGEPOWER', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='DP_NORMAL', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_CRIT', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_AVOID', index=2, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_ACCURACY', index=3, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_BLOCK', index=4, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_SLIP', index=5, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_WUDI', index=6, number=7, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DP_HP_CRIT', index=7, number=10, options=None, type=None)], containing_type=None, options=None, serialized_start=2675, serialized_end=2803)
DAMAGEPOWER = enum_type_wrapper.EnumTypeWrapper(_DAMAGEPOWER)
_DAMAGESOURCE = _descriptor.EnumDescriptor(name='DAMAGESOURCE', full_name='skillresult.DAMAGESOURCE', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='DM_SKILL_EFFECT', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='DM_SKILL_REFLECT', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=2805, serialized_end=2862)
DAMAGESOURCE = enum_type_wrapper.EnumTypeWrapper(_DAMAGESOURCE)
DM_ADD = 0
DM_SUB = 1
DM_NONE = 2
DM_CRI = 3
DP_NORMAL = 0
DP_CRIT = 1
DP_AVOID = 3
DP_ACCURACY = 4
DP_BLOCK = 5
DP_SLIP = 6
DP_WUDI = 7
DP_HP_CRIT = 10
DM_SKILL_EFFECT = 0
DM_SKILL_REFLECT = 1
_MOVEPARAM = _descriptor.Descriptor(name='MoveParam', full_name='skillresult.MoveParam', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='refId', full_name='skillresult.MoveParam.refId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='srcPos', full_name='skillresult.MoveParam.srcPos', index=1, number=2, type=2, cpp_type=6, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')),
 _descriptor.FieldDescriptor(name='distFixType', full_name='skillresult.MoveParam.distFixType', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='distFixVal', full_name='skillresult.MoveParam.distFixVal', index=3, number=4, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=34, serialized_end=121)
_SPECIALEFFECT = _descriptor.Descriptor(name='SpecialEffect', full_name='skillresult.SpecialEffect', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='seid', full_name='skillresult.SpecialEffect.seid', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='seType', full_name='skillresult.SpecialEffect.seType', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='seValue', full_name='skillresult.SpecialEffect.seValue', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=123, serialized_end=185)
_DMGABSORBVALUE = _descriptor.Descriptor(name='DmgAbsorbValue', full_name='skillresult.DmgAbsorbValue', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='value', full_name='skillresult.DmgAbsorbValue.value', index=0, number=1, type=4, cpp_type=4, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='source', full_name='skillresult.DmgAbsorbValue.source', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='srcid', full_name='skillresult.DmgAbsorbValue.srcid', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=187, serialized_end=249)
_DMGABSORB = _descriptor.Descriptor(name='DmgAbsorb', full_name='skillresult.DmgAbsorb', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='elements', full_name='skillresult.DmgAbsorb.elements', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=251, serialized_end=309)
_RESULT = _descriptor.Descriptor(name='Result', full_name='skillresult.Result', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='srcid', full_name='skillresult.Result.srcid', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmgSource', full_name='skillresult.Result.dmgSource', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmgSourceId', full_name='skillresult.Result.dmgSourceId', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmgs', full_name='skillresult.Result.dmgs', index=3, number=4, type=4, cpp_type=4, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')),
 _descriptor.FieldDescriptor(name='hps', full_name='skillresult.Result.hps', index=4, number=5, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mps', full_name='skillresult.Result.mps', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='eps', full_name='skillresult.Result.eps', index=6, number=7, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmgAbsorb', full_name='skillresult.Result.dmgAbsorb', index=7, number=8, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='ars', full_name='skillresult.Result.ars', index=8, number=9, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='seId', full_name='skillresult.Result.seId', index=9, number=10, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='labours', full_name='skillresult.Result.labours', index=10, number=11, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='comboNum', full_name='skillresult.Result.comboNum', index=11, number=12, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='comboDmg', full_name='skillresult.Result.comboDmg', index=12, number=13, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='healAbsorb', full_name='skillresult.Result.healAbsorb', index=13, number=14, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=312, serialized_end=652)
_CONTROLLSTATEDATA = _descriptor.Descriptor(name='ControllStateData', full_name='skillresult.ControllStateData', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='controllStateId', full_name='skillresult.ControllStateData.controllStateId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='controllStateHit', full_name='skillresult.ControllStateData.controllStateHit', index=1, number=2, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=654, serialized_end=724)
_FENSHENVAL = _descriptor.Descriptor(name='FenshenVal', full_name='skillresult.FenshenVal', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='id', full_name='skillresult.FenshenVal.id', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='fenshenPos', full_name='skillresult.FenshenVal.fenshenPos', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='tgtPos', full_name='skillresult.FenshenVal.tgtPos', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='yaw', full_name='skillresult.FenshenVal.yaw', index=3, number=4, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=726, serialized_end=845)
_RESULTSET = _descriptor.Descriptor(name='ResultSet', full_name='skillresult.ResultSet', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='eid', full_name='skillresult.ResultSet.eid', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.ResultSet.results', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='moveId', full_name='skillresult.ResultSet.moveId', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='moveTime', full_name='skillresult.ResultSet.moveTime', index=3, number=4, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='moveParam', full_name='skillresult.ResultSet.moveParam', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='kill', full_name='skillresult.ResultSet.kill', index=5, number=6, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='realDmg', full_name='skillresult.ResultSet.realDmg', index=6, number=7, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='controllStateData', full_name='skillresult.ResultSet.controllStateData', index=7, number=8, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='addFlagStates', full_name='skillresult.ResultSet.addFlagStates', index=8, number=9, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dispellFlagStates', full_name='skillresult.ResultSet.dispellFlagStates', index=9, number=10, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='fenshen', full_name='skillresult.ResultSet.fenshen', index=10, number=11, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=848, serialized_end=1196)
_POSITION = _descriptor.Descriptor(name='Position', full_name='skillresult.Position', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='x', full_name='skillresult.Position.x', index=0, number=1, type=2, cpp_type=6, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='y', full_name='skillresult.Position.y', index=1, number=2, type=2, cpp_type=6, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='z', full_name='skillresult.Position.z', index=2, number=3, type=2, cpp_type=6, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1198, serialized_end=1241)
_FLAGSTATEVAL = _descriptor.Descriptor(name='FlagStateVal', full_name='skillresult.FlagStateVal', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='flagStateId', full_name='skillresult.FlagStateVal.flagStateId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='lastTime', full_name='skillresult.FlagStateVal.lastTime', index=1, number=2, type=2, cpp_type=6, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1243, serialized_end=1296)
_SKILLRESULT = _descriptor.Descriptor(name='SkillResult', full_name='skillresult.SkillResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='tgtId', full_name='skillresult.SkillResult.tgtId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='num', full_name='skillresult.SkillResult.num', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='lv', full_name='skillresult.SkillResult.lv', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.SkillResult.results', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='isInstantSkill', full_name='skillresult.SkillResult.isInstantSkill', index=4, number=5, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='pos', full_name='skillresult.SkillResult.pos', index=5, number=6, type=2, cpp_type=6, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')),
 _descriptor.FieldDescriptor(name='dontPlayAction', full_name='skillresult.SkillResult.dontPlayAction', index=6, number=7, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='guideCastTime', full_name='skillresult.SkillResult.guideCastTime', index=7, number=8, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cd', full_name='skillresult.SkillResult.cd', index=8, number=9, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='gcd', full_name='skillresult.SkillResult.gcd', index=9, number=10, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='timeStamp', full_name='skillresult.SkillResult.timeStamp', index=10, number=11, type=1, cpp_type=5, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1299, serialized_end=1525)
_PSKILLRESULT = _descriptor.Descriptor(name='PSkillResult', full_name='skillresult.PSkillResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='pskillId', full_name='skillresult.PSkillResult.pskillId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='pskillLv', full_name='skillresult.PSkillResult.pskillLv', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='results', full_name='skillresult.PSkillResult.results', index=2, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1527, serialized_end=1618)
_ATTACKRESULT = _descriptor.Descriptor(name='AttackResult', full_name='skillresult.AttackResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='tgtId', full_name='skillresult.AttackResult.tgtId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.AttackResult.results', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='resultType', full_name='skillresult.AttackResult.resultType', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dontPlayAction', full_name='skillresult.AttackResult.dontPlayAction', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='nextAtkDelay', full_name='skillresult.AttackResult.nextAtkDelay', index=4, number=5, type=2, cpp_type=6, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1621, serialized_end=1757)
_MFRESULT = _descriptor.Descriptor(name='MFResult', full_name='skillresult.MFResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='magicfieldId', full_name='skillresult.MFResult.magicfieldId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='num', full_name='skillresult.MFResult.num', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='lv', full_name='skillresult.MFResult.lv', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.MFResult.results', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='skillId', full_name='skillresult.MFResult.skillId', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='skillLv', full_name='skillresult.MFResult.skillLv', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='rPosList', full_name='skillresult.MFResult.rPosList', index=6, number=7, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1760, serialized_end=1933)
_FENSHENRESULT = _descriptor.Descriptor(name='FenshenResult', full_name='skillresult.FenshenResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='fenshenId', full_name='skillresult.FenshenResult.fenshenId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.FenshenResult.results', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='skillId', full_name='skillresult.FenshenResult.skillId', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='skillLv', full_name='skillresult.FenshenResult.skillLv', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1935, serialized_end=2044)
_GUIDESKILLRESULT = _descriptor.Descriptor(name='GuideSkillResult', full_name='skillresult.GuideSkillResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='tgtId', full_name='skillresult.GuideSkillResult.tgtId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='num', full_name='skillresult.GuideSkillResult.num', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='lv', full_name='skillresult.GuideSkillResult.lv', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='results', full_name='skillresult.GuideSkillResult.results', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='pos', full_name='skillresult.GuideSkillResult.pos', index=4, number=5, type=2, cpp_type=6, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), ''))], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2046, serialized_end=2162)
_COMBATMESSAGEARG = _descriptor.Descriptor(name='CombatMessageArg', full_name='skillresult.CombatMessageArg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='d', full_name='skillresult.CombatMessageArg.d', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='s', full_name='skillresult.CombatMessageArg.s', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2164, serialized_end=2204)
_COMBATMESSAGE = _descriptor.Descriptor(name='CombatMessage', full_name='skillresult.CombatMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='num', full_name='skillresult.CombatMessage.num', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='args', full_name='skillresult.CombatMessage.args', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg0', full_name='skillresult.CombatMessage.dmg0', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg1', full_name='skillresult.CombatMessage.dmg1', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg2', full_name='skillresult.CombatMessage.dmg2', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg3', full_name='skillresult.CombatMessage.dmg3', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg4', full_name='skillresult.CombatMessage.dmg4', index=6, number=7, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg5', full_name='skillresult.CombatMessage.dmg5', index=7, number=8, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg6', full_name='skillresult.CombatMessage.dmg6', index=8, number=9, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg7', full_name='skillresult.CombatMessage.dmg7', index=9, number=10, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dmg', full_name='skillresult.CombatMessage.dmg', index=10, number=11, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='toall', full_name='skillresult.CombatMessage.toall', index=11, number=12, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2207, serialized_end=2420)
_STATERESULT = _descriptor.Descriptor(name='StateResult', full_name='skillresult.StateResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='details', full_name='skillresult.StateResult.details', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2422, serialized_end=2480)
_STATEMESSAGES = _descriptor.Descriptor(name='StateMessages', full_name='skillresult.StateMessages', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='stateId', full_name='skillresult.StateMessages.stateId', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='stateSrc', full_name='skillresult.StateMessages.stateSrc', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='stateTgt', full_name='skillresult.StateMessages.stateTgt', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='addHp', full_name='skillresult.StateMessages.addHp', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='reduceHp', full_name='skillresult.StateMessages.reduceHp', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='addMp', full_name='skillresult.StateMessages.addMp', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='reduceMp', full_name='skillresult.StateMessages.reduceMp', index=6, number=7, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2483, serialized_end=2617)
_DMGABSORB.fields_by_name['elements'].message_type = _DMGABSORBVALUE
_RESULT.fields_by_name['dmgSource'].enum_type = _DAMAGESOURCE
_RESULT.fields_by_name['dmgAbsorb'].message_type = _DMGABSORB
_RESULT.fields_by_name['ars'].enum_type = _DAMAGEPOWER
_RESULT.fields_by_name['healAbsorb'].message_type = _DMGABSORB
_FENSHENVAL.fields_by_name['fenshenPos'].message_type = _POSITION
_FENSHENVAL.fields_by_name['tgtPos'].message_type = _POSITION
_RESULTSET.fields_by_name['results'].message_type = _RESULT
_RESULTSET.fields_by_name['moveParam'].message_type = _MOVEPARAM
_RESULTSET.fields_by_name['controllStateData'].message_type = _CONTROLLSTATEDATA
_RESULTSET.fields_by_name['addFlagStates'].message_type = _FLAGSTATEVAL
_RESULTSET.fields_by_name['fenshen'].message_type = _FENSHENVAL
_SKILLRESULT.fields_by_name['results'].message_type = _RESULTSET
_PSKILLRESULT.fields_by_name['results'].message_type = _RESULTSET
_ATTACKRESULT.fields_by_name['results'].message_type = _RESULTSET
_MFRESULT.fields_by_name['results'].message_type = _RESULTSET
_MFRESULT.fields_by_name['rPosList'].message_type = _POSITION
_FENSHENRESULT.fields_by_name['results'].message_type = _RESULTSET
_GUIDESKILLRESULT.fields_by_name['results'].message_type = _RESULTSET
_COMBATMESSAGE.fields_by_name['args'].message_type = _COMBATMESSAGEARG
_STATERESULT.fields_by_name['details'].message_type = _STATEMESSAGES
DESCRIPTOR.message_types_by_name['MoveParam'] = _MOVEPARAM
DESCRIPTOR.message_types_by_name['SpecialEffect'] = _SPECIALEFFECT
DESCRIPTOR.message_types_by_name['DmgAbsorbValue'] = _DMGABSORBVALUE
DESCRIPTOR.message_types_by_name['DmgAbsorb'] = _DMGABSORB
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['ControllStateData'] = _CONTROLLSTATEDATA
DESCRIPTOR.message_types_by_name['FenshenVal'] = _FENSHENVAL
DESCRIPTOR.message_types_by_name['ResultSet'] = _RESULTSET
DESCRIPTOR.message_types_by_name['Position'] = _POSITION
DESCRIPTOR.message_types_by_name['FlagStateVal'] = _FLAGSTATEVAL
DESCRIPTOR.message_types_by_name['SkillResult'] = _SKILLRESULT
DESCRIPTOR.message_types_by_name['PSkillResult'] = _PSKILLRESULT
DESCRIPTOR.message_types_by_name['AttackResult'] = _ATTACKRESULT
DESCRIPTOR.message_types_by_name['MFResult'] = _MFRESULT
DESCRIPTOR.message_types_by_name['FenshenResult'] = _FENSHENRESULT
DESCRIPTOR.message_types_by_name['GuideSkillResult'] = _GUIDESKILLRESULT
DESCRIPTOR.message_types_by_name['CombatMessageArg'] = _COMBATMESSAGEARG
DESCRIPTOR.message_types_by_name['CombatMessage'] = _COMBATMESSAGE
DESCRIPTOR.message_types_by_name['StateResult'] = _STATERESULT
DESCRIPTOR.message_types_by_name['StateMessages'] = _STATEMESSAGES

class MoveParam(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MOVEPARAM


class SpecialEffect(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SPECIALEFFECT


class DmgAbsorbValue(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DMGABSORBVALUE


class DmgAbsorb(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DMGABSORB


class Result(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RESULT


class ControllStateData(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CONTROLLSTATEDATA


class FenshenVal(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FENSHENVAL


class ResultSet(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RESULTSET


class Position(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _POSITION


class FlagStateVal(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FLAGSTATEVAL


class SkillResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SKILLRESULT


class PSkillResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PSKILLRESULT


class AttackResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ATTACKRESULT


class MFResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MFRESULT


class FenshenResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FENSHENRESULT


class GuideSkillResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GUIDESKILLRESULT


class CombatMessageArg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _COMBATMESSAGEARG


class CombatMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _COMBATMESSAGE


class StateResult(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STATERESULT


class StateMessages(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STATEMESSAGES


_MOVEPARAM.fields_by_name['srcPos'].has_options = True
_MOVEPARAM.fields_by_name['srcPos']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')
_RESULT.fields_by_name['dmgs'].has_options = True
_RESULT.fields_by_name['dmgs']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')
_SKILLRESULT.fields_by_name['pos'].has_options = True
_SKILLRESULT.fields_by_name['pos']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')
_GUIDESKILLRESULT.fields_by_name['pos'].has_options = True
_GUIDESKILLRESULT.fields_by_name['pos']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '')
