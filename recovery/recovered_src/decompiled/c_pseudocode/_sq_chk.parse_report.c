// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C3460(
        _QWORD *a1,
        __int64 a2,
        _QWORD **a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8)
{
  __int64 v8; // rbx
  _QWORD *v9; // r12
  __int64 v11; // rax
  __int64 v12; // rdx
  __int64 v13; // rax
  __int64 v14; // rdx
  _QWORD *v15; // rax
  __int64 v16; // rax
  _QWORD *v17; // rbp
  __int64 v18; // rax
  bool v19; // zf
  _QWORD *v20; // rdi
  _QWORD *v21; // rbp
  __int64 v22; // rdx
  int v23; // eax
  int v24; // r14d
  __int64 v25; // rax
  __int64 v26; // rdx
  __int64 v27; // rbx
  _QWORD *v28; // rcx
  __int64 v30; // r13
  __int64 v31; // r14
  int v32; // edx
  __int64 v33; // r15
  __int64 v34; // rax
  __int64 v35; // rbp
  __int64 v36; // rax
  __int64 v37; // rdx
  unsigned __int64 v38; // r8
  __int128 v39; // xmm0
  __int64 v40; // rax
  __int64 v41; // rax
  __int64 v42; // rdx
  __int64 v43; // rbx
  _QWORD *v44; // rcx
  __int64 v45; // rdx
  int v46; // eax
  int v47; // r13d
  __int64 v48; // rbp
  int v49; // eax
  __int64 v50; // rax
  __int64 v51; // r13
  __int64 v52; // rcx
  __int64 v53; // rax
  _QWORD *v54; // rbp
  __int64 v55; // rax
  _QWORD *v56; // r13
  __int64 v57; // rax
  _QWORD *v58; // rbp
  __int64 v59; // rax
  __int64 v60; // rax
  __int64 v61; // rdx
  unsigned __int64 v62; // r8
  __int128 v63; // xmm0
  __int64 v64; // rax
  __int64 v65; // r8
  __int64 v66; // rax
  __int64 v67; // rax
  __int64 *v68; // rax
  __int64 *v69; // rax
  __int64 v70; // rax
  int v71; // [rsp+C4h] [rbp+2Ch]
  int v72; // [rsp+C4h] [rbp+2Ch]

  v8 = qword_1439440E0;
  v9 = *a3;
  if ( qword_1439440E0 == 0 )
    goto LABEL_4;
  v11 = *(_QWORD *)qword_1439440E0;
  if ( *(__int64 *)qword_1439440E0 > 1 )
  {
    *(_QWORD *)qword_1439440E0 = v11 - 1;
LABEL_4:
    qword_1439440E0 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_1439440D8,
                        a3: qword_143944160,
                        a4: 16);
    v8 = qword_1439440E0;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_1439440E0 + 16) != 0 )
  {
    v34 = v11 - 1;
    *(_QWORD *)qword_1439440E0 = v34;
    if ( v34 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_1439440E0 + 8) + 48LL))(a1: qword_1439440E0);
    goto LABEL_4;
  }
LABEL_5:
  v12 = a1[7];
  v13 = *(_QWORD *)(v12 + 8);
  *(_QWORD *)(v8 + 120) = v13;
  *(_QWORD *)(v12 + 8) = v8 + 72;
  if ( v13 != 0
    && (*(_BYTE *)(v13 + 69) == 1
     || *(_QWORD *)(v13 + 56) >= (unsigned __int64)(*(_QWORD *)(v13 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v13 + 32) + 168LL)
                                                  + 184)) )
  {
    v14 = *(_QWORD *)(v8 + 112);
    if ( v14 != 0 )
    {
      v15 = *(_QWORD **)(v13 + 40);
      *(_QWORD *)(v14 + 16) = v15;
      if ( v15 != nullptr )
        ++*v15;
    }
  }
  ++*(_QWORD *)v8;
  *(_DWORD *)(v8 + 64) = 0;
  v16 = MEMORY[0x13B054620](a1, a2: v9, a3: qword_14393FD60);
  v17 = (_QWORD *)v16;
  if ( v16 == 0 )
  {
    v30 = a1[12];
    v31 = a1[13];
    v20 = nullptr;
    v33 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    v32 = 157;
    a1[14] = 0;
    goto LABEL_36;
  }
  v18 = MEMORY[0x13B054620](a1, a2: v16, a3: qword_14393FEC8);
  v19 = (*v17)-- == 1;
  v20 = (_QWORD *)v18;
  if ( !v19 )
  {
    if ( v18 != 0 )
      goto LABEL_14;
LABEL_31:
    v30 = a1[12];
    v31 = a1[13];
    v32 = 157;
    v33 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_36;
  }
  (*(void (__fastcall **)(_QWORD *))(v17[1] + 48LL))(a1: v17);
  if ( v20 == nullptr )
    goto LABEL_31;
LABEL_14:
  v21 = (_QWORD *)qword_143A35170(a1: v20);
  if ( v21 == nullptr )
  {
LABEL_35:
    v33 = a1[14];
    a1[14] = 0;
    v32 = 158;
    v30 = a1[12];
    v31 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_36;
  }
  v22 = ((__int64 (*)(void))unk_14321A720)();
  if ( v22 == 0 )
  {
    v65 = qword_14393FE20;
    goto LABEL_85;
  }
  v23 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1432B17A0)(a1: v21, a2: v22);
  v19 = (*v21)-- == 1;
  v24 = v23;
  if ( v19 )
    (*(void (__fastcall **)(_QWORD *))(v21[1] + 48LL))(a1: v21);
  if ( v24 == -1 )
    goto LABEL_35;
  if ( v24 != 1 )
    goto LABEL_20;
  v21 = (_QWORD *)qword_143A35170(a1: v20);
  if ( v21 == nullptr )
    goto LABEL_35;
  v45 = ((__int64 (*)(void))unk_14321A330)();
  if ( v45 == 0 )
  {
    v65 = qword_14393FED0;
LABEL_85:
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: v65);
    v30 = a6;
    v31 = a7;
    v32 = 158;
    v33 = a8;
    v19 = (*v21)-- == 1;
    if ( v19 )
    {
      (*(void (__fastcall **)(_QWORD *))(v21[1] + 48LL))(a1: v21);
      v32 = 158;
    }
    goto LABEL_36;
  }
  v46 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1432B17A0)(a1: v21, a2: v45);
  v19 = (*v21)-- == 1;
  v47 = v46;
  if ( v19 )
    (*(void (__fastcall **)(_QWORD *))(v21[1] + 48LL))(a1: v21);
  if ( v47 == -1 )
    goto LABEL_35;
  if ( v47 != 1 )
  {
LABEL_20:
    v25 = a1[7];
    v26 = *(_QWORD *)(v25 + 8);
    v27 = *(_QWORD *)(v26 + 40);
    v28 = *(_QWORD **)(v27 + 16);
    *(_QWORD *)(v25 + 8) = *(_QWORD *)(v26 + 48);
    *(_DWORD *)(v27 + 64) = -1;
    if ( v28 != nullptr )
    {
      *(_QWORD *)(v27 + 16) = 0;
      v19 = (*v28)-- == 1;
      if ( v19 )
        (*(void (**)(void))(v28[1] + 48LL))();
    }
    v19 = (*(_QWORD *)v27)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v27 + 8) + 48LL))(a1: v27);
    *(_QWORD *)(v27 + 120) = 0;
    ++*(_QWORD *)qword_143A35618;
    v19 = (*v20)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(_QWORD *))(v20[1] + 48LL))(a1: v20);
    v19 = (*v9)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
    return qword_143A35618;
  }
  v48 = *(_QWORD *)(*(_QWORD *)&qword_14393FD08[0] + 32LL);
  if ( *(_BYTE *)(v48 + 10) == 0 )
  {
    v68 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)&qword_14393FD08[0], a2: qword_14393FEE0);
    if ( v68 != nullptr )
    {
      v52 = *v68;
      goto LABEL_93;
    }
LABEL_94:
    v69 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393FEE0);
    if ( v69 == nullptr || (v52 = *v69, *v69 == 0) )
    {
      ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393FEE0);
      v30 = a6;
      v31 = a7;
      v32 = 161;
      v33 = a8;
      goto LABEL_36;
    }
    goto LABEL_72;
  }
  v49 = *(_DWORD *)(v48 + 12);
  if ( v49 == 0 )
  {
    v49 = dword_143547A4C;
    *(_DWORD *)(v48 + 12) = dword_143547A4C++;
  }
  if ( dword_143547A3C == v49 )
  {
    v50 = qword_1439440D0;
  }
  else
  {
    dword_143547A3C = v49;
    v50 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v48,
            a2: qword_14393FEE0,
            a3: *(_QWORD *)(qword_14393FEE0 + 24));
    qword_1439440D0 = v50;
  }
  if ( v50 < 0 )
    goto LABEL_94;
  v51 = v48 + (1LL << *(_BYTE *)(v48 + 9)) + 32;
  v52 = *(_QWORD *)(v51 + 16 * v50 + 8);
  if ( v52 == 0 )
  {
    v70 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v48,
            a2: qword_14393FEE0,
            a3: *(_QWORD *)(qword_14393FEE0 + 24));
    qword_1439440D0 = v70;
    if ( v70 < 0 )
      goto LABEL_94;
    v52 = *(_QWORD *)(v51 + 16 * v70 + 8);
LABEL_93:
    if ( v52 == 0 )
      goto LABEL_94;
  }
LABEL_72:
  v53 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v52, a2: qword_14393FEE8);
  v54 = (_QWORD *)v53;
  if ( v53 != 0 )
  {
    v55 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v53, a2: qword_14393FEF0);
    v19 = (*v54)-- == 1;
    v56 = (_QWORD *)v55;
    if ( v19 )
      (*(void (__fastcall **)(_QWORD *))(v54[1] + 48LL))(a1: v54);
    if ( v56 != nullptr )
    {
      *(_DWORD *)(v8 + 40) = 161;
      v57 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64, _QWORD))unk_1430D9050)(
              a1,
              a2: v56,
              a3: qword_14393FEF8,
              a4: *(_QWORD *)(qword_14393FF00 + 24));
      v19 = (*v56)-- == 1;
      v58 = (_QWORD *)v57;
      if ( v19 )
        (*(void (__fastcall **)(_QWORD *))(v56[1] + 48LL))(a1: v56);
      if ( v58 != nullptr )
      {
        v19 = (*v58)-- == 1;
        if ( v19 )
          (*(void (__fastcall **)(_QWORD *))(v58[1] + 48LL))(a1: v58);
        goto LABEL_20;
      }
    }
  }
  v30 = a1[12];
  v31 = a1[13];
  v32 = 161;
  v33 = a1[14];
  *((_OWORD *)a1 + 6) = 0;
  a1[14] = 0;
LABEL_36:
  if ( v33 != 0 )
  {
    if ( *(_QWORD *)(v33 + 24) != v8 )
    {
      v35 = *(_QWORD *)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v35;
        *(_QWORD *)v35 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v71 = v32;
        v66 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
        v32 = v71;
        v35 = v66;
      }
      *(_QWORD *)(v35 + 24) = v8;
      ++*(_QWORD *)v8;
      v36 = *(_QWORD *)(qword_143A35A28 + 504);
      *(_DWORD *)(v35 + 36) = v32;
      *(_DWORD *)(v35 + 32) = -1;
      v37 = *(_QWORD *)(*(_QWORD *)(v36 + 16) + 744LL);
      v38 = *(_QWORD *)(v37 + 8);
      *(_QWORD *)&v39 = v37;
      v40 = v38 | *(_QWORD *)(v35 - 8) & 3LL;
      *(_QWORD *)v38 = v35 - 16;
      *((_QWORD *)&v39 + 1) = v40;
      *(_OWORD *)(v35 - 16) = v39;
      v19 = *(_QWORD *)v33 == 0;
      *(_QWORD *)(v37 + 8) = v35 - 16;
      *(_QWORD *)(v35 + 16) = v33;
      if ( v19 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v33 + 8) + 48LL))(a1: v33);
      v33 = v35;
    }
  }
  else
  {
    v33 = *(_QWORD *)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v33;
      *(_QWORD *)v33 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v72 = v32;
      v67 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
      v32 = v72;
      v33 = v67;
    }
    *(_QWORD *)(v33 + 16) = 0;
    *(_QWORD *)(v33 + 24) = v8;
    ++*(_QWORD *)v8;
    v59 = *(_QWORD *)(qword_143A35A28 + 504);
    *(_DWORD *)(v33 + 36) = v32;
    v60 = *(_QWORD *)(v59 + 16);
    *(_DWORD *)(v33 + 32) = -1;
    v61 = *(_QWORD *)(v60 + 744);
    v62 = *(_QWORD *)(v61 + 8);
    *(_QWORD *)&v63 = v61;
    v64 = v62 | *(_QWORD *)(v33 - 8) & 3LL;
    *(_QWORD *)v62 = v33 - 16;
    *((_QWORD *)&v63 + 1) = v64;
    *(_OWORD *)(v33 - 16) = v63;
    *(_QWORD *)(v61 + 8) = v33 - 16;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *, _QWORD *))unk_142F544C0)(a1: v8, a2: &unk_14359FC67, a3: v9, a4: v20);
  if ( qword_1439440E0 == v8 )
  {
    v19 = (*(_QWORD *)v8)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v8 + 8) + 48LL))(a1: v8);
    qword_1439440E0 = 0;
  }
  v41 = a1[7];
  v42 = *(_QWORD *)(v41 + 8);
  v43 = *(_QWORD *)(v42 + 40);
  v44 = *(_QWORD **)(v43 + 16);
  *(_QWORD *)(v41 + 8) = *(_QWORD *)(v42 + 48);
  *(_DWORD *)(v43 + 64) = -1;
  if ( v44 != nullptr )
  {
    *(_QWORD *)(v43 + 16) = 0;
    v19 = (*v44)-- == 1;
    if ( v19 )
      (*(void (**)(void))(v44[1] + 48LL))();
  }
  v19 = (*(_QWORD *)v43)-- == 1;
  if ( v19 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v43 + 8) + 48LL))(a1: v43);
  *(_QWORD *)(v43 + 120) = 0;
  if ( v20 != nullptr )
  {
    v19 = (*v20)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(_QWORD *))(v20[1] + 48LL))(a1: v20);
  }
  v19 = (*v9)-- == 1;
  if ( v19 )
    (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
  MEMORY[0x13B00DF80](a1, a2: v30, a3: v31, a4: v33);
  return 0;
}