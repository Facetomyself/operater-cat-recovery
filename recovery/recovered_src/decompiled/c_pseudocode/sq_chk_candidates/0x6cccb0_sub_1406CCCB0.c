// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406CCCB0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6)
{
  __int64 v6; // rbx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 v10; // rax
  __int64 v11; // rdx
  _QWORD *v12; // rax
  __int64 v13; // rsi
  int v14; // eax
  __int64 v15; // rax
  __int64 v16; // rbp
  __int64 v17; // rax
  _QWORD *v18; // rsi
  int v19; // ebp
  __int64 v20; // rdx
  __int64 v21; // rbx
  __int64 v22; // rax
  __int64 v23; // rdx
  __int64 v24; // rdi
  _QWORD *v25; // rcx
  bool v26; // zf
  _QWORD *v28; // rax
  int v29; // r15d
  __int64 v30; // r12
  __int64 v31; // r13
  __int64 v32; // rbp
  __int64 v33; // r14
  __int64 v34; // rax
  __int64 v35; // rdx
  unsigned __int64 v36; // r8
  __int128 v37; // xmm0
  __int64 v38; // rax
  __int64 v39; // rax
  __int64 v40; // rdx
  __int64 v41; // rbx
  _QWORD *v42; // rcx
  __int64 v43; // rax
  __int64 v44; // rsi
  int v45; // eax
  __int64 v46; // rax
  __int64 v47; // rbp
  __int64 v48; // rdx
  __int64 v49; // rax
  __int64 v50; // rax
  _QWORD *v51; // r14
  __int64 v52; // rsi
  int v53; // eax
  __int64 v54; // rax
  __int64 v55; // r12
  __int64 v56; // rbp
  __int64 v57; // rsi
  int v58; // eax
  __int64 v59; // rax
  __int64 v60; // r12
  __int64 v61; // rax
  __int64 v62; // rax
  __int64 *v63; // rax
  __int64 *v64; // rcx
  __int64 v65; // rax
  __int64 *v66; // rax
  __int64 v67; // rdx
  __int64 *v68; // rax
  __int64 *v69; // rax
  __int64 v70; // rax
  __int64 v71; // rax
  __int64 v72; // rdx
  unsigned __int64 v73; // r8
  __int128 v74; // xmm0
  __int64 v75; // rax
  __int64 v76; // rax
  _QWORD *v77; // rcx
  __int64 *v78; // rax
  __int64 *v79; // rax
  __int64 v80; // r8
  __int64 v81; // rax
  __int64 *v82; // rax
  __int64 *v83; // rax
  __int64 v84; // rax
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // [rsp+A8h] [rbp+20h] BYREF

  v6 = qword_143943D60;
  if ( qword_143943D60 == 0 )
    goto LABEL_4;
  v8 = *(_QWORD *)qword_143943D60;
  if ( *(__int64 *)qword_143943D60 > 1 )
  {
    *(_QWORD *)qword_143943D60 = v8 - 1;
LABEL_4:
    qword_143943D60 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F10,
                        a3: qword_143943E90,
                        a4: 8);
    v6 = qword_143943D60;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943D60 + 16) != 0 )
  {
    v43 = v8 - 1;
    *(_QWORD *)qword_143943D60 = v43;
    if ( v43 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943D60 + 8) + 48LL))(a1: qword_143943D60);
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
    if ( dword_1435479F8 == v14 )
    {
      v15 = qword_143943D40;
      if ( qword_143943D40 < 0 )
        goto LABEL_33;
    }
    else
    {
      dword_1435479F8 = v14;
      v15 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v13,
              a2: qword_14393F7E0,
              a3: *(_QWORD *)(qword_14393F7E0 + 24));
      qword_143943D40 = v15;
      if ( v15 < 0 )
        goto LABEL_33;
    }
    v16 = v13 + (1LL << *(_BYTE *)(v13 + 9)) + 32;
    if ( *(_QWORD *)(v16 + 16 * v15 + 8) != 0 )
      goto LABEL_17;
    v81 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v13,
            a2: qword_14393F7E0,
            a3: *(_QWORD *)(qword_14393F7E0 + 24));
    qword_143943D40 = v81;
    if ( v81 >= 0 )
    {
      v67 = *(_QWORD *)(v16 + 16 * v81 + 8);
LABEL_96:
      if ( v67 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v66 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F7E0);
    if ( v66 != nullptr )
    {
      v67 = *v66;
      goto LABEL_96;
    }
  }
LABEL_33:
  v28 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F7E0);
  if ( v28 == nullptr || *v28 == 0 )
  {
    v29 = 312;
    v18 = nullptr;
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v87, a3: qword_14393F7E0);
    v30 = v87;
    v31 = a5;
    v32 = a6;
    goto LABEL_36;
  }
LABEL_17:
  *(_DWORD *)(v6 + 40) = 312;
  v17 = ((__int64 (__fastcall *)(_QWORD *))unk_142F69C20)(a1);
  v18 = (_QWORD *)v17;
  if ( v17 == 0 )
  {
    v30 = a1[12];
    v31 = a1[13];
    v29 = 312;
    v32 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_36;
  }
  v19 = MEMORY[0x13B01B050](a1: v17);
  v20 = *v18 - 1LL;
  if ( v19 == -1 )
  {
    v30 = a1[12];
    v31 = a1[13];
    v32 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    *v18 = v20;
    if ( v20 != 0 )
    {
      v29 = 312;
      v18 = nullptr;
    }
    else
    {
      v76 = v18[1];
      v77 = v18;
      v29 = 312;
      v18 = nullptr;
      (*(void (__fastcall **)(_QWORD *))(v76 + 48))(a1: v77);
    }
    goto LABEL_36;
  }
  *v18 = v20;
  if ( v20 == 0 )
    (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
  if ( v19 == 0 )
  {
    v21 = qword_143A35200;
    v18 = nullptr;
    ++*(_QWORD *)qword_143A35200;
LABEL_23:
    v22 = a1[7];
    v23 = *(_QWORD *)(v22 + 8);
    v24 = *(_QWORD *)(v23 + 40);
    v25 = *(_QWORD **)(v24 + 16);
    *(_QWORD *)(v22 + 8) = *(_QWORD *)(v23 + 48);
    *(_DWORD *)(v24 + 64) = -1;
    if ( v25 != nullptr )
    {
      *(_QWORD *)(v24 + 16) = 0;
      v26 = (*v25)-- == 1;
      if ( v26 )
        (*(void (**)(void))(v25[1] + 48LL))();
    }
    v26 = (*(_QWORD *)v24)-- == 1;
    if ( v26 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v24 + 8) + 48LL))(a1: v24);
    *(_QWORD *)(v24 + 120) = 0;
    if ( v18 != nullptr )
    {
      v26 = (*v18)-- == 1;
      if ( v26 )
        (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
    }
    return v21;
  }
  v44 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v44 + 10) != 0 )
  {
    v45 = *(_DWORD *)(v44 + 12);
    if ( v45 == 0 )
    {
      v45 = dword_143547A28;
      *(_DWORD *)(v44 + 12) = dword_143547A28++;
    }
    if ( dword_1435479FC == v45 )
    {
      v46 = qword_143943D48;
    }
    else
    {
      dword_1435479FC = v45;
      v46 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v44,
              a2: qword_14393F960,
              a3: *(_QWORD *)(qword_14393F960 + 24));
      qword_143943D48 = v46;
    }
    if ( v46 >= 0 )
    {
      v47 = v44 + (1LL << *(_BYTE *)(v44 + 9)) + 32;
      v48 = *(_QWORD *)(v47 + 16 * v46 + 8);
      if ( v48 != 0 )
        goto LABEL_63;
      v84 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v44,
              a2: qword_14393F960,
              a3: *(_QWORD *)(qword_14393F960 + 24));
      qword_143943D48 = v84;
      if ( v84 >= 0 )
      {
        v48 = *(_QWORD *)(v47 + 16 * v84 + 8);
LABEL_100:
        if ( v48 != 0 )
          goto LABEL_63;
      }
    }
  }
  else
  {
    v68 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F960);
    if ( v68 != nullptr )
    {
      v48 = *v68;
      goto LABEL_100;
    }
  }
  v69 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F960);
  if ( v69 == nullptr || (v48 = *v69, *v69 == 0) )
  {
    v29 = 313;
    v18 = nullptr;
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v87, a3: qword_14393F960);
    v30 = v87;
    v31 = a5;
    v32 = a6;
    goto LABEL_36;
  }
LABEL_63:
  *(_DWORD *)(v6 + 40) = 313;
  v49 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_1430D8EF0)(a1, a2: v48, a3: qword_14393F968);
  v18 = (_QWORD *)v49;
  if ( v49 == 0 )
  {
LABEL_131:
    v30 = a1[12];
    v31 = a1[13];
    v29 = 313;
    v32 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_36;
  }
  v50 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v49, a2: qword_14393F970);
  v26 = (*v18)-- == 1;
  v51 = (_QWORD *)v50;
  if ( v26 )
    (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
  if ( v51 == nullptr )
  {
    v30 = a1[12];
    v31 = a1[13];
    v18 = nullptr;
    v32 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    v29 = 313;
    a1[14] = 0;
    goto LABEL_36;
  }
  v52 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v52 + 10) != 0 )
  {
    v53 = *(_DWORD *)(v52 + 12);
    if ( v53 == 0 )
    {
      v53 = dword_143547A28;
      *(_DWORD *)(v52 + 12) = dword_143547A28++;
    }
    if ( dword_143547A00 == v53 )
    {
      v54 = qword_143943D50;
    }
    else
    {
      dword_143547A00 = v53;
      v54 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v52,
              a2: qword_14393F978,
              a3: *(_QWORD *)(qword_14393F978 + 24));
      qword_143943D50 = v54;
    }
    if ( v54 >= 0 )
    {
      v55 = v52 + (1LL << *(_BYTE *)(v52 + 9)) + 32;
      v56 = *(_QWORD *)(v55 + 16 * v54 + 8);
      if ( v56 != 0 )
        goto LABEL_74;
      v85 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v52,
              a2: qword_14393F978,
              a3: *(_QWORD *)(qword_14393F978 + 24));
      qword_143943D50 = v85;
      if ( v85 >= 0 )
      {
        v56 = *(_QWORD *)(v55 + 16 * v85 + 8);
LABEL_112:
        if ( v56 != 0 )
          goto LABEL_74;
      }
    }
  }
  else
  {
    v78 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F978);
    if ( v78 != nullptr )
    {
      v56 = *v78;
      goto LABEL_112;
    }
  }
  v79 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F978);
  if ( v79 == nullptr || (v56 = *v79, *v79 == 0) )
  {
    v80 = qword_14393F978;
    goto LABEL_125;
  }
LABEL_74:
  v57 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v57 + 10) != 0 )
  {
    v58 = *(_DWORD *)(v57 + 12);
    if ( v58 == 0 )
    {
      v58 = dword_143547A28;
      *(_DWORD *)(v57 + 12) = dword_143547A28++;
    }
    if ( dword_143547A04 == v58 )
    {
      v59 = qword_143943D58;
    }
    else
    {
      dword_143547A04 = v58;
      v59 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v57,
              a2: qword_14393F980,
              a3: *(_QWORD *)(qword_14393F980 + 24));
      qword_143943D58 = v59;
    }
    if ( v59 >= 0 )
    {
      v60 = v57 + (1LL << *(_BYTE *)(v57 + 9)) + 32;
      v61 = *(_QWORD *)(v60 + 16 * v59 + 8);
      if ( v61 != 0 )
        goto LABEL_81;
      v86 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v57,
              a2: qword_14393F980,
              a3: *(_QWORD *)(qword_14393F980 + 24));
      qword_143943D58 = v86;
      if ( v86 >= 0 )
      {
        v61 = *(_QWORD *)(v60 + 16 * v86 + 8);
LABEL_121:
        if ( v61 != 0 )
          goto LABEL_81;
      }
    }
  }
  else
  {
    v82 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F980);
    if ( v82 != nullptr )
    {
      v61 = *v82;
      goto LABEL_121;
    }
  }
  v83 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F980);
  if ( v83 == nullptr || (v61 = *v83) == 0 )
  {
    v80 = qword_14393F980;
LABEL_125:
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v87, a3: v80);
    v30 = v87;
    v31 = a5;
    v32 = a6;
    v26 = (*v51)-- == 1;
    v29 = 313;
    v18 = nullptr;
    if ( v26 )
      (*(void (__fastcall **)(_QWORD *))(v51[1] + 48LL))(a1: v51);
    goto LABEL_36;
  }
LABEL_81:
  *(_DWORD *)(v6 + 40) = 313;
  v87 = v56;
  a5 = v61;
  v62 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64 *))unk_142F79F60)(a1, a2: v51, a3: &v87);
  v26 = (*v51)-- == 1;
  v18 = (_QWORD *)v62;
  if ( v26 )
    (*(void (__fastcall **)(_QWORD *))(v51[1] + 48LL))(a1: v51);
  if ( v18 == nullptr )
    goto LABEL_131;
  v63 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, _QWORD *))unk_142F5B7C0)(a1, a2: v18);
  v64 = v63;
  if ( v63 != nullptr )
  {
    v65 = *v63 - 1;
    v26 = v64[2] == 0;
    *v64 = v65;
    if ( v26 )
    {
      if ( v65 == 0 )
        (*(void (**)(void))(v64[1] + 48))();
      v21 = qword_143A35208;
      ++*(_QWORD *)qword_143A35208;
    }
    else
    {
      if ( v65 == 0 )
        (*(void (**)(void))(v64[1] + 48))();
      v21 = qword_143A35200;
      ++*(_QWORD *)qword_143A35200;
    }
    goto LABEL_23;
  }
  v30 = a1[12];
  v31 = a1[13];
  v29 = 314;
  v32 = a1[14];
  *((_OWORD *)a1 + 6) = 0;
  a1[14] = 0;
LABEL_36:
  if ( v32 != 0 )
  {
    if ( *(_QWORD *)(v32 + 24) != v6 )
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
        v33 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      *(_QWORD *)(v33 + 24) = v6;
      ++*(_QWORD *)v6;
      v34 = *(_QWORD *)(qword_143A35A28 + 504);
      *(_DWORD *)(v33 + 32) = -1;
      *(_DWORD *)(v33 + 36) = v29;
      v35 = *(_QWORD *)(*(_QWORD *)(v34 + 16) + 744LL);
      v36 = *(_QWORD *)(v35 + 8);
      *(_QWORD *)&v37 = v35;
      v38 = v36 | *(_QWORD *)(v33 - 8) & 3LL;
      *(_QWORD *)v36 = v33 - 16;
      *((_QWORD *)&v37 + 1) = v38;
      *(_OWORD *)(v33 - 16) = v37;
      v26 = *(_QWORD *)v32 == 0;
      *(_QWORD *)(v35 + 8) = v33 - 16;
      *(_QWORD *)(v33 + 16) = v32;
      if ( v26 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v32 + 8) + 48LL))(a1: v32);
      v32 = v33;
    }
  }
  else
  {
    v32 = *(_QWORD *)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v32;
      *(_QWORD *)v32 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v32 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
    }
    *(_QWORD *)(v32 + 16) = 0;
    *(_QWORD *)(v32 + 24) = v6;
    ++*(_QWORD *)v6;
    v70 = *(_QWORD *)(qword_143A35A28 + 504);
    *(_DWORD *)(v32 + 32) = -1;
    v71 = *(_QWORD *)(v70 + 16);
    *(_DWORD *)(v32 + 36) = v29;
    v72 = *(_QWORD *)(v71 + 744);
    v73 = *(_QWORD *)(v72 + 8);
    *(_QWORD *)&v74 = v72;
    v75 = v73 | *(_QWORD *)(v32 - 8) & 3LL;
    *(_QWORD *)v73 = v32 - 16;
    *((_QWORD *)&v74 + 1) = v75;
    *(_OWORD *)(v32 - 16) = v74;
    *(_QWORD *)(v72 + 8) = v32 - 16;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v6, a2: &unk_14359FC65, a3: v18);
  if ( qword_143943D60 == v6 )
  {
    v26 = (*(_QWORD *)v6)-- == 1;
    if ( v26 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943D60 = 0;
  }
  v39 = a1[7];
  v40 = *(_QWORD *)(v39 + 8);
  v41 = *(_QWORD *)(v40 + 40);
  v42 = *(_QWORD **)(v41 + 16);
  *(_QWORD *)(v39 + 8) = *(_QWORD *)(v40 + 48);
  *(_DWORD *)(v41 + 64) = -1;
  if ( v42 != nullptr )
  {
    *(_QWORD *)(v41 + 16) = 0;
    v26 = (*v42)-- == 1;
    if ( v26 )
      (*(void (**)(void))(v42[1] + 48LL))();
  }
  v26 = (*(_QWORD *)v41)-- == 1;
  if ( v26 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v41 + 8) + 48LL))(a1: v41);
  *(_QWORD *)(v41 + 120) = 0;
  if ( v18 != nullptr )
  {
    v26 = (*v18)-- == 1;
    if ( v26 )
      (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
  }
  MEMORY[0x13B00DF80](a1, a2: v30, a3: v31, a4: v32);
  return 0;
}