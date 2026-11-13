// write access to const memory has been detected, the output may be wrong!
void __fastcall sub_14067A530(
        __int64 a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8,
        __int64 *a9,
        _QWORD *a10,
        __int64 a11,
        __int64 a12)
{
  _QWORD *v12; // rbx
  __int64 v13; // rdi
  __int64 v14; // rsi
  __int64 v15; // r12
  _QWORD *v16; // r13
  _QWORD *v17; // r14
  _QWORD *v18; // r15
  __int64 v19; // rax
  __int64 v20; // rdx
  __int64 v21; // rbx
  _QWORD *v22; // rcx
  bool v23; // zf
  __int64 v25; // [rsp+48h] [rbp+48h]

  (*(void (__fastcall **)(__int64))(*(_QWORD *)(a2 + 8) + 48LL))(a1: a2);
  ((void (__fastcall *)(_QWORD *, void *, _QWORD *, __int64 *))unk_142F544C0)(
    a1: v12,
    a2: &unk_14359FDAF,
    a3: a10,
    a4: a9);
  if ( (_QWORD *)qword_143944AD8 == v12 )
  {
    v23 = (*v12)-- == 1;
    if ( v23 )
      (*(void (__fastcall **)(_QWORD *))(v12[1] + 48LL))(a1: v12);
    qword_143944AD8 = 0;
  }
  v19 = *(_QWORD *)(v14 + 56);
  v20 = *(_QWORD *)(v19 + 8);
  v21 = *(_QWORD *)(v20 + 40);
  v22 = *(_QWORD **)(v21 + 16);
  *(_QWORD *)(v19 + 8) = *(_QWORD *)(v20 + 48);
  *(_DWORD *)(v21 + 64) = -1;
  if ( v22 != nullptr )
  {
    *(_QWORD *)(v21 + 16) = 0;
    v23 = (*v22)-- == 1;
    if ( v23 )
      (*(void (**)(void))(v22[1] + 48LL))();
  }
  v23 = (*(_QWORD *)v21)-- == 1;
  if ( v23 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v21 + 8) + 48LL))(a1: v21);
  *(_QWORD *)(v21 + 120) = 0;
  if ( a9 != nullptr )
  {
    v25 = *a9;
    *a9 = v25 - 1;
    if ( v25 == 1 )
      (*(void (__fastcall **)(__int64 *))(a9[1] + 48))(a1: a9);
  }
  if ( v18 != nullptr )
  {
    v23 = (*v18)-- == 1;
    if ( v23 )
      (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
  }
  if ( v16 != nullptr )
  {
    v23 = (*v16)-- == 1;
    if ( v23 )
      (*(void (__fastcall **)(_QWORD *))(v16[1] + 48LL))(a1: v16);
  }
  if ( v17 != nullptr )
  {
    v23 = (*v17)-- == 1;
    if ( v23 )
      (*(void (__fastcall **)(_QWORD *))(v17[1] + 48LL))(a1: v17);
  }
  v23 = (*a10)-- == 1;
  if ( v23 )
    (*(void (__fastcall **)(_QWORD *))(a10[1] + 48LL))(a1: a10);
  MEMORY[0x13B00DF80](a1: v14, a2: v13, a3: a12, a4: v15);
  JUMPOUT(0x140679DDALL);
}