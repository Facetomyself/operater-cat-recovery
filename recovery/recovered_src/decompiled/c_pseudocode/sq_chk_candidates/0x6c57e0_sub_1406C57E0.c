// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C57E0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, _QWORD *a6)
{
  __int64 v6; // rbx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 v10; // rax
  __int64 v11; // rdx
  _QWORD *v12; // rax
  __int64 v13; // rdi
  int v14; // eax
  __int64 v15; // rax
  __int64 v16; // rbp
  __int64 v17; // rdi
  __int64 v18; // rax
  __int64 v19; // rdx
  __int64 v20; // rbx
  _QWORD *v21; // rcx
  bool v22; // zf
  _QWORD *v24; // rax
  __int64 v25; // r12
  __int64 v26; // r13
  _QWORD *v27; // rdi
  __int64 v28; // rax
  _QWORD *v29; // rbp
  __int64 v30; // rdx
  unsigned __int64 v31; // r8
  __int128 v32; // xmm0
  __int64 v33; // rax
  __int64 v34; // rax
  __int64 v35; // rdx
  __int64 v36; // rbx
  _QWORD *v37; // rcx
  __int64 *v38; // rax
  __int64 v39; // rdx
  __int64 v40; // rdx
  unsigned __int64 v41; // r8
  __int128 v42; // xmm0
  __int64 v43; // rax
  __int64 v44; // rax
  __int64 v45; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143944008;
  if ( qword_143944008 == 0 )
    goto LABEL_4;
  v8 = *(_QWORD *)qword_143944008;
  if ( *(__int64 *)qword_143944008 > 1 )
  {
    *(_QWORD *)qword_143944008 = v8 - 1;
LABEL_4:
    qword_143944008 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, _QWORD))unk_142F58E90)(
                        a1,
                        a2: qword_143944000,
                        a3: qword_1439440A8,
                        a4: 0);
    v6 = qword_143944008;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143944008 + 16) != 0 )
  {
    v28 = v8 - 1;
    *(_QWORD *)qword_143944008 = v28;
    if ( v28 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143944008 + 8) + 48LL))(a1: qword_143944008);
    goto LABEL_4;
  }
LABEL_5:
  v9 = a1[7];
  v10 = *(_QWORD *)(v9 + 8);
  *(_QWORD *)(v6 + 120) = v10;
  *(_QWORD *)(v9 + 8) = v6 + 72;
  if ( v10 != 0
    && (*(_BYTE *)(v10 + 69) == 1
     || *(_QWORD *)(v10 + 56) >= (unsigned __int64)(*(_QWORD *)(v10 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v10 + 32) + 168LL)
                                                  + 184)) )
  {
    v11 = *(_QWORD *)(v6 + 112);
    if ( v11 != 0 )
    {
      v12 = *(_QWORD **)(v10 + 40);
      *(_QWORD *)(v11 + 16) = v12;
      if ( v12 != nullptr )
        ++*v12;
    }
  }
  ++*(_QWORD *)v6;
  *(_DWORD *)(v6 + 64) = 0;
  v13 = *(_QWORD *)(qword_143944018 + 32);
  if ( *(_BYTE *)(v13 + 10) != 0 )
  {
    v14 = *(_DWORD *)(v13 + 12);
    if ( v14 == 0 )
    {
      v14 = dword_143547A34;
      *(_DWORD *)(v13 + 12) = dword_143547A34++;
    }
    if ( dword_143547A30 == v14 )
    {
      v15 = qword_143943FF8;
      if ( qword_143943FF8 < 0 )
        goto LABEL_25;
    }
    else
    {
      dword_143547A30 = v14;
      v15 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v13,
              a2: qword_143944028,
              a3: *(_QWORD *)(qword_143944028 + 24));
      qword_143943FF8 = v15;
      if ( v15 < 0 )
        goto LABEL_25;
    }
    v16 = v13 + (1LL << *(_BYTE *)(v13 + 9)) + 32;
    if ( *(_QWORD *)(v16 + 16 * v15 + 8) != 0 )
      goto LABEL_17;
    v44 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v13,
            a2: qword_143944028,
            a3: *(_QWORD *)(qword_143944028 + 24));
    qword_143943FF8 = v44;
    if ( v44 >= 0 )
    {
      v39 = *(_QWORD *)(v16 + 16 * v44 + 8);
LABEL_51:
      if ( v39 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v38 = (__int64 *)MEMORY[0x13B02A410](a1: qword_143944018, a2: qword_143944028);
    if ( v38 != nullptr )
    {
      v39 = *v38;
      goto LABEL_51;
    }
  }
LABEL_25:
  v24 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_143944028);
  if ( v24 == nullptr || *v24 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v45, a3: qword_143944028);
    v25 = v45;
    v26 = a5;
    v27 = a6;
    goto LABEL_32;
  }
LABEL_17:
  *(_DWORD *)(v6 + 40) = 13;
  v17 = ((__int64 (__fastcall *)(_QWORD *))unk_142F69C20)(a1);
  if ( v17 != 0 )
  {
    v18 = a1[7];
    v19 = *(_QWORD *)(v18 + 8);
    v20 = *(_QWORD *)(v19 + 40);
    v21 = *(_QWORD **)(v20 + 16);
    *(_QWORD *)(v18 + 8) = *(_QWORD *)(v19 + 48);
    *(_DWORD *)(v20 + 64) = -1;
    if ( v21 != nullptr )
    {
      *(_QWORD *)(v20 + 16) = 0;
      v22 = (*v21)-- == 1;
      if ( v22 )
        (*(void (**)(void))(v21[1] + 48LL))();
    }
    v22 = (*(_QWORD *)v20)-- == 1;
    if ( v22 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v20 + 8) + 48LL))(a1: v20);
    *(_QWORD *)(v20 + 120) = 0;
    return v17;
  }
  v27 = (_QWORD *)a1[14];
  a1[14] = 0;
  v25 = a1[12];
  v26 = a1[13];
  *((_OWORD *)a1 + 6) = 0;
LABEL_32:
  if ( v27 != nullptr )
  {
    if ( v27[3] != v6 )
    {
      v29 = *(_QWORD **)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *v29;
        *v29 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v29 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      v29[3] = v6;
      ++*(_QWORD *)v6;
      v29[4] = qword_1435A0578;
      v30 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v31 = *(_QWORD *)(v30 + 8);
      *(_QWORD *)&v32 = v30;
      v33 = v31 | *(v29 - 1) & 3LL;
      *(_QWORD *)v31 = v29 - 2;
      *((_QWORD *)&v32 + 1) = v33;
      *((_OWORD *)v29 - 1) = v32;
      v22 = *v27 == 0;
      *(_QWORD *)(v30 + 8) = v29 - 2;
      v29[2] = v27;
      if ( v22 )
        (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
      v27 = v29;
    }
  }
  else
  {
    v27 = *(_QWORD **)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *v27;
      *v27 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v27 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
    }
    v27[2] = 0;
    v27[3] = v6;
    ++*(_QWORD *)v6;
    v27[4] = qword_1435A0578;
    v40 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v41 = *(_QWORD *)(v40 + 8);
    *(_QWORD *)&v42 = v40;
    v43 = v41 | *(v27 - 1) & 3LL;
    *(_QWORD *)v41 = v27 - 2;
    *((_QWORD *)&v42 + 1) = v43;
    *((_OWORD *)v27 - 1) = v42;
    *(_QWORD *)(v40 + 8) = v27 - 2;
  }
  ((void (__fastcall *)(__int64, _QWORD))unk_142F544C0)(a1: v6, a2: 0);
  if ( qword_143944008 == v6 )
  {
    v22 = (*(_QWORD *)v6)-- == 1;
    if ( v22 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143944008 = 0;
  }
  v34 = a1[7];
  v35 = *(_QWORD *)(v34 + 8);
  v36 = *(_QWORD *)(v35 + 40);
  v37 = *(_QWORD **)(v36 + 16);
  *(_QWORD *)(v34 + 8) = *(_QWORD *)(v35 + 48);
  *(_DWORD *)(v36 + 64) = -1;
  if ( v37 != nullptr )
  {
    *(_QWORD *)(v36 + 16) = 0;
    v22 = (*v37)-- == 1;
    if ( v22 )
      (*(void (**)(void))(v37[1] + 48LL))();
  }
  v22 = (*(_QWORD *)v36)-- == 1;
  if ( v22 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v36 + 8) + 48LL))(a1: v36);
  *(_QWORD *)(v36 + 120) = 0;
  MEMORY[0x13B00DF80](a1, a2: v25, a3: v26, a4: v27);
  return 0;
}