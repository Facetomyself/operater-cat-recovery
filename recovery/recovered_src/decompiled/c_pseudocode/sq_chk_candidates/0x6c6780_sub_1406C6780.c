// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C6780(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, _QWORD *a6)
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
  __int64 v17; // rdx
  __int64 v18; // rdi
  __int64 v19; // rax
  __int64 v20; // rdx
  __int64 v21; // rbx
  _QWORD *v22; // rcx
  bool v23; // zf
  __int64 *v25; // rax
  __int64 v26; // r12
  __int64 v27; // r13
  _QWORD *v28; // rdi
  __int64 v29; // rax
  _QWORD *v30; // rbp
  __int64 v31; // rdx
  unsigned __int64 v32; // r8
  __int128 v33; // xmm0
  __int64 v34; // rax
  __int64 v35; // rax
  __int64 v36; // rdx
  __int64 v37; // rbx
  _QWORD *v38; // rcx
  __int64 *v39; // rax
  __int64 v40; // rdx
  unsigned __int64 v41; // r8
  __int128 v42; // xmm0
  __int64 v43; // rax
  __int64 v44; // rax
  __int64 v45; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143943E98;
  if ( qword_143943E98 == 0 )
    goto LABEL_4;
  v8 = *(_QWORD *)qword_143943E98;
  if ( *(__int64 *)qword_143943E98 > 1 )
  {
    *(_QWORD *)qword_143943E98 = v8 - 1;
LABEL_4:
    qword_143943E98 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, _QWORD))unk_142F58E90)(
                        a1,
                        a2: qword_143943FA0,
                        a3: qword_143943E90,
                        a4: 0);
    v6 = qword_143943E98;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E98 + 16) != 0 )
  {
    v29 = v8 - 1;
    *(_QWORD *)qword_143943E98 = v29;
    if ( v29 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E98 + 8) + 48LL))(a1: qword_143943E98);
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
  v13 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v13 + 10) != 0 )
  {
    v14 = *(_DWORD *)(v13 + 12);
    if ( v14 == 0 )
    {
      v14 = dword_143547A28;
      *(_DWORD *)(v13 + 12) = dword_143547A28++;
    }
    if ( dword_143547A2C == v14 )
    {
      v15 = qword_143943E88;
      if ( qword_143943E88 < 0 )
        goto LABEL_25;
    }
    else
    {
      dword_143547A2C = v14;
      v15 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v13,
              a2: qword_14393F600,
              a3: *(_QWORD *)(qword_14393F600 + 24));
      qword_143943E88 = v15;
      if ( v15 < 0 )
        goto LABEL_25;
    }
    v16 = v13 + (1LL << *(_BYTE *)(v13 + 9)) + 32;
    v17 = *(_QWORD *)(v16 + 16 * v15 + 8);
    if ( v17 != 0 )
      goto LABEL_17;
    v44 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v13,
            a2: qword_14393F600,
            a3: *(_QWORD *)(qword_14393F600 + 24));
    qword_143943E88 = v44;
    if ( v44 >= 0 )
    {
      v17 = *(_QWORD *)(v16 + 16 * v44 + 8);
LABEL_51:
      if ( v17 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v39 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F600);
    if ( v39 != nullptr )
    {
      v17 = *v39;
      goto LABEL_51;
    }
  }
LABEL_25:
  v25 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F600);
  if ( v25 == nullptr || (v17 = *v25, *v25 == 0) )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v45, a3: qword_14393F600);
    v26 = v45;
    v27 = a5;
    v28 = a6;
    goto LABEL_32;
  }
LABEL_17:
  *(_DWORD *)(v6 + 40) = 25;
  v18 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_1430D8EF0)(a1, a2: v17, a3: qword_14393F608);
  if ( v18 != 0 )
  {
    v19 = a1[7];
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
    return v18;
  }
  v28 = (_QWORD *)a1[14];
  a1[14] = 0;
  v26 = a1[12];
  v27 = a1[13];
  *((_OWORD *)a1 + 6) = 0;
LABEL_32:
  if ( v28 != nullptr )
  {
    if ( v28[3] != v6 )
    {
      v30 = *(_QWORD **)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *v30;
        *v30 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v30 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      v30[3] = v6;
      ++*(_QWORD *)v6;
      v30[4] = qword_1435A0580;
      v31 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v32 = *(_QWORD *)(v31 + 8);
      *(_QWORD *)&v33 = v31;
      v34 = v32 | *(v30 - 1) & 3LL;
      *(_QWORD *)v32 = v30 - 2;
      *((_QWORD *)&v33 + 1) = v34;
      *((_OWORD *)v30 - 1) = v33;
      v23 = *v28 == 0;
      *(_QWORD *)(v31 + 8) = v30 - 2;
      v30[2] = v28;
      if ( v23 )
        (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
      v28 = v30;
    }
  }
  else
  {
    v28 = *(_QWORD **)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *v28;
      *v28 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v28 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
    }
    v28[2] = 0;
    v28[3] = v6;
    ++*(_QWORD *)v6;
    v28[4] = qword_1435A0580;
    v40 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v41 = *(_QWORD *)(v40 + 8);
    *(_QWORD *)&v42 = v40;
    v43 = v41 | *(v28 - 1) & 3LL;
    *(_QWORD *)v41 = v28 - 2;
    *((_QWORD *)&v42 + 1) = v43;
    *((_OWORD *)v28 - 1) = v42;
    *(_QWORD *)(v40 + 8) = v28 - 2;
  }
  ((void (__fastcall *)(__int64, _QWORD))unk_142F544C0)(a1: v6, a2: 0);
  if ( qword_143943E98 == v6 )
  {
    v23 = (*(_QWORD *)v6)-- == 1;
    if ( v23 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943E98 = 0;
  }
  v35 = a1[7];
  v36 = *(_QWORD *)(v35 + 8);
  v37 = *(_QWORD *)(v36 + 40);
  v38 = *(_QWORD **)(v37 + 16);
  *(_QWORD *)(v35 + 8) = *(_QWORD *)(v36 + 48);
  *(_DWORD *)(v37 + 64) = -1;
  if ( v38 != nullptr )
  {
    *(_QWORD *)(v37 + 16) = 0;
    v23 = (*v38)-- == 1;
    if ( v23 )
      (*(void (**)(void))(v38[1] + 48LL))();
  }
  v23 = (*(_QWORD *)v37)-- == 1;
  if ( v23 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v37 + 8) + 48LL))(a1: v37);
  *(_QWORD *)(v37 + 120) = 0;
  MEMORY[0x13B00DF80](a1, a2: v26, a3: v27, a4: v28);
  return 0;
}