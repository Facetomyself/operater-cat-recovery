// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C6C60(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, _QWORD *a6)
{
  __int64 v6; // rbx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 v10; // rax
  __int64 v11; // rdx
  _QWORD *v12; // rax
  __int64 v13; // rdx
  __int64 *v14; // rdi
  __int64 v15; // rax
  bool v16; // zf
  _QWORD *v17; // rbp
  __int64 v18; // rdi
  int v19; // eax
  __int64 v20; // rax
  __int64 v21; // r12
  __int64 v22; // rax
  __int64 v23; // rdi
  __int64 v24; // rax
  __int64 v25; // rdx
  __int64 v26; // rbx
  _QWORD *v27; // rcx
  _QWORD *v29; // r13
  __int64 v30; // rdi
  __int64 v31; // r12
  _QWORD *v32; // rbp
  __int64 v33; // rdx
  unsigned __int64 v34; // r8
  __int128 v35; // xmm0
  __int64 v36; // rax
  __int64 v37; // rax
  __int64 v38; // rdx
  __int64 v39; // rbx
  _QWORD *v40; // rcx
  __int64 v41; // rax
  _QWORD *v42; // rax
  __int64 v43; // rax
  __int64 v44; // rdx
  unsigned __int64 v45; // r8
  __int128 v46; // xmm0
  __int64 v47; // rax
  __int64 *v48; // rax
  __int64 v49; // rdx
  __int64 v50; // rax
  __int64 v51; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143943E80;
  if ( qword_143943E80 == 0 )
    goto LABEL_4;
  v8 = *(_QWORD *)qword_143943E80;
  if ( *(__int64 *)qword_143943E80 > 1 )
  {
    *(_QWORD *)qword_143943E80 = v8 - 1;
LABEL_4:
    qword_143943E80 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, _QWORD))unk_142F58E90)(
                        a1,
                        a2: qword_143943EB8,
                        a3: qword_143943E90,
                        a4: 0);
    v6 = qword_143943E80;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E80 + 16) != 0 )
  {
    v41 = v8 - 1;
    *(_QWORD *)qword_143943E80 = v41;
    if ( v41 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E80 + 8) + 48LL))(a1: qword_143943E80);
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
  v13 = ((__int64 (*)(void))unk_14321A200)();
  if ( v13 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v51, a3: qword_14393F610);
    v30 = v51;
    v31 = a5;
    v29 = a6;
    goto LABEL_33;
  }
  *(_DWORD *)(v6 + 40) = 32;
  v14 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_142F69C20)(a1, a2: v13);
  if ( v14 == nullptr )
    goto LABEL_32;
  if ( v14[1] == qword_143A35788 )
  {
    v17 = (_QWORD *)((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F52DC0)(
                      a1: *(_QWORD *)(qword_143A35A28 + 504),
                      a2: v14,
                      a3: qword_14393F618);
    v43 = *v14 - 1;
    *v14 = v43;
    if ( v17 == nullptr )
    {
      if ( v43 == 0 )
        (*(void (__fastcall **)(__int64 *))(v14[1] + 48))(a1: v14);
      goto LABEL_32;
    }
    if ( v43 == 0 )
      (*(void (__fastcall **)(__int64 *))(v14[1] + 48))(a1: v14);
    goto LABEL_16;
  }
  v15 = ((__int64 (__fastcall *)(__int64 *, __int64))unk_1430DB780)(a1: v14, a2: qword_14393F618);
  v16 = (*v14)-- == 1;
  v17 = (_QWORD *)v15;
  if ( v16 )
  {
    (*(void (__fastcall **)(__int64 *))(v14[1] + 48))(a1: v14);
    if ( v17 == nullptr )
      goto LABEL_32;
LABEL_16:
    v18 = *(_QWORD *)(qword_14393F5F8 + 32);
    if ( *(_BYTE *)(v18 + 10) != 0 )
    {
      v19 = *(_DWORD *)(v18 + 12);
      if ( v19 == 0 )
      {
        v19 = dword_143547A28;
        *(_DWORD *)(v18 + 12) = dword_143547A28++;
      }
      if ( dword_143547A24 == v19 )
      {
        v20 = qword_143943E78;
        if ( qword_143943E78 < 0 )
          goto LABEL_51;
      }
      else
      {
        dword_143547A24 = v19;
        v20 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                a1: v18,
                a2: qword_14393F620,
                a3: *(_QWORD *)(qword_14393F620 + 24));
        qword_143943E78 = v20;
        if ( v20 < 0 )
          goto LABEL_51;
      }
      v21 = v18 + (1LL << *(_BYTE *)(v18 + 9)) + 32;
      if ( *(_QWORD *)(v21 + 16 * v20 + 8) != 0 )
        goto LABEL_22;
      v50 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v18,
              a2: qword_14393F620,
              a3: *(_QWORD *)(qword_14393F620 + 24));
      qword_143943E78 = v50;
      if ( v50 < 0 )
      {
LABEL_51:
        v42 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F620);
        if ( v42 == nullptr || *v42 == 0 )
        {
          ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v51, a3: qword_14393F620);
          v16 = (*v17)-- == 1;
          v30 = v51;
          v31 = a5;
          v29 = a6;
          if ( v16 )
            (*(void (__fastcall **)(_QWORD *))(v17[1] + 48LL))(a1: v17);
          goto LABEL_33;
        }
        goto LABEL_22;
      }
      v49 = *(_QWORD *)(v21 + 16 * v50 + 8);
    }
    else
    {
      v48 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F620);
      if ( v48 == nullptr )
        goto LABEL_51;
      v49 = *v48;
    }
    if ( v49 != 0 )
    {
LABEL_22:
      v22 = ((__int64 (__fastcall *)(_QWORD *))unk_1430DBC90)(a1: v17);
      v16 = (*v17)-- == 1;
      v23 = v22;
      if ( v16 )
        (*(void (__fastcall **)(_QWORD *))(v17[1] + 48LL))(a1: v17);
      if ( v23 != 0 )
      {
        v24 = a1[7];
        v25 = *(_QWORD *)(v24 + 8);
        v26 = *(_QWORD *)(v25 + 40);
        v27 = *(_QWORD **)(v26 + 16);
        *(_QWORD *)(v24 + 8) = *(_QWORD *)(v25 + 48);
        *(_DWORD *)(v26 + 64) = -1;
        if ( v27 != nullptr )
        {
          *(_QWORD *)(v26 + 16) = 0;
          v16 = (*v27)-- == 1;
          if ( v16 )
            (*(void (**)(void))(v27[1] + 48LL))();
        }
        v16 = (*(_QWORD *)v26)-- == 1;
        if ( v16 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v26 + 8) + 48LL))(a1: v26);
        *(_QWORD *)(v26 + 120) = 0;
        return v23;
      }
      goto LABEL_32;
    }
    goto LABEL_51;
  }
  if ( v15 != 0 )
    goto LABEL_16;
LABEL_32:
  v29 = (_QWORD *)a1[14];
  a1[14] = 0;
  v30 = a1[12];
  v31 = a1[13];
  *((_OWORD *)a1 + 6) = 0;
LABEL_33:
  if ( v29 != nullptr )
  {
    if ( v29[3] != v6 )
    {
      v32 = *(_QWORD **)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *v32;
        *v32 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v32 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      v32[3] = v6;
      ++*(_QWORD *)v6;
      v32[4] = qword_1435A0450;
      v33 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v34 = *(_QWORD *)(v33 + 8);
      *(_QWORD *)&v35 = v33;
      v36 = v34 | *(v32 - 1) & 3LL;
      *(_QWORD *)v34 = v32 - 2;
      *((_QWORD *)&v35 + 1) = v36;
      *((_OWORD *)v32 - 1) = v35;
      v16 = *v29 == 0;
      *(_QWORD *)(v33 + 8) = v32 - 2;
      v32[2] = v29;
      if ( v16 )
        (*(void (__fastcall **)(_QWORD *))(v29[1] + 48LL))(a1: v29);
      v29 = v32;
    }
  }
  else
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
    v29[2] = 0;
    v29[3] = v6;
    ++*(_QWORD *)v6;
    v29[4] = qword_1435A0450;
    v44 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v45 = *(_QWORD *)(v44 + 8);
    *(_QWORD *)&v46 = v44;
    v47 = v45 | *(v29 - 1) & 3LL;
    *(_QWORD *)v45 = v29 - 2;
    *((_QWORD *)&v46 + 1) = v47;
    *((_OWORD *)v29 - 1) = v46;
    *(_QWORD *)(v44 + 8) = v29 - 2;
  }
  ((void (__fastcall *)(__int64, _QWORD))unk_142F544C0)(a1: v6, a2: 0);
  if ( qword_143943E80 == v6 )
  {
    v16 = (*(_QWORD *)v6)-- == 1;
    if ( v16 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943E80 = 0;
  }
  v37 = a1[7];
  v38 = *(_QWORD *)(v37 + 8);
  v39 = *(_QWORD *)(v38 + 40);
  v40 = *(_QWORD **)(v39 + 16);
  *(_QWORD *)(v37 + 8) = *(_QWORD *)(v38 + 48);
  *(_DWORD *)(v39 + 64) = -1;
  if ( v40 != nullptr )
  {
    *(_QWORD *)(v39 + 16) = 0;
    v16 = (*v40)-- == 1;
    if ( v16 )
      (*(void (**)(void))(v40[1] + 48LL))();
  }
  v16 = (*(_QWORD *)v39)-- == 1;
  if ( v16 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v39 + 8) + 48LL))(a1: v39);
  *(_QWORD *)(v39 + 120) = 0;
  MEMORY[0x13B00DF80](a1, a2: v30, a3: v31, a4: v29);
  return 0;
}