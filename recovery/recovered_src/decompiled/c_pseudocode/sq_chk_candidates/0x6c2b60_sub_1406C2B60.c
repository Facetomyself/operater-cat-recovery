// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C2B60(
        _QWORD *a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8,
        __int64 a9,
        __int64 a10,
        __int64 a11,
        __int64 a12)
{
  __int64 v12; // r13
  __int64 v13; // r14
  __int64 v14; // rbx
  __int64 v16; // rax
  __int64 v17; // rdx
  __int64 v18; // rax
  __int64 v19; // rdx
  _QWORD *v20; // rax
  _QWORD *v21; // rdi
  __int64 v22; // rax
  _QWORD *v23; // rdx
  __int64 v24; // rax
  _QWORD *v25; // rbp
  __int64 v26; // rcx
  bool v27; // zf
  _QWORD *v28; // rax
  _QWORD *v29; // rcx
  __int64 v30; // rcx
  _QWORD *v31; // rax
  _QWORD *v32; // r13
  __int64 v33; // rcx
  __int64 v34; // rax
  _QWORD *v35; // rbp
  __int64 v36; // rax
  _QWORD *v37; // r15
  __int64 v38; // rbp
  int v39; // eax
  __int64 v40; // rax
  __int64 v41; // r13
  int v42; // eax
  int v43; // ebp
  __int64 v44; // rbx
  __int64 v45; // rax
  __int64 v46; // rax
  __int64 v47; // rdx
  __int64 v48; // rsi
  _QWORD *v49; // rcx
  __int64 v51; // rbp
  int v52; // edx
  __int64 v53; // r12
  __int64 v54; // rax
  __int64 v55; // rdx
  unsigned __int64 v56; // r8
  __int128 v57; // xmm0
  __int64 v58; // rax
  __int64 v59; // rax
  __int64 v60; // rdx
  __int64 v61; // rbx
  _QWORD *v62; // rcx
  _QWORD *v63; // rax
  __int64 v64; // rax
  __int64 v65; // rax
  __int64 v66; // rdx
  unsigned __int64 v67; // r8
  __int128 v68; // xmm0
  __int64 v69; // rax
  __int64 *v70; // rax
  __int64 v71; // rdx
  _QWORD *v72; // rax
  __int64 v73; // rax
  __int64 v74; // rax
  __int64 v75; // rax
  int v76; // [rsp+F4h] [rbp+3Ch]
  int v77; // [rsp+F4h] [rbp+3Ch]

  v14 = qword_143944108;
  if ( qword_143944108 == 0 )
    goto LABEL_4;
  v16 = *(_QWORD *)qword_143944108;
  if ( *(__int64 *)qword_143944108 > 1 )
  {
    *(_QWORD *)qword_143944108 = v16 - 1;
LABEL_4:
    qword_143944108 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143944100,
                        a3: qword_143944160,
                        a4: 8);
    v14 = qword_143944108;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143944108 + 16) != 0 )
  {
    v45 = v16 - 1;
    *(_QWORD *)qword_143944108 = v45;
    if ( v45 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143944108 + 8) + 48LL))(a1: qword_143944108);
    goto LABEL_4;
  }
LABEL_5:
  v17 = a1[7];
  v18 = *(_QWORD *)(v17 + 8);
  *(_QWORD *)(v14 + 120) = v18;
  *(_QWORD *)(v17 + 8) = v14 + 72;
  if ( v18 != 0
    && (*(_BYTE *)(v18 + 69) == 1
     || *(_QWORD *)(v18 + 56) >= (unsigned __int64)(*(_QWORD *)(v18 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v18 + 32) + 168LL)
                                                  + 184)) )
  {
    v19 = *(_QWORD *)(v14 + 112);
    if ( v19 != 0 )
    {
      v20 = *(_QWORD **)(v18 + 40);
      *(_QWORD *)(v19 + 16) = v20;
      if ( v20 != nullptr )
        ++*v20;
    }
  }
  v21 = (_QWORD *)qword_1435FA6E0;
  *(_DWORD *)(v14 + 64) = 0;
  ++*(_QWORD *)v14;
  v22 = *(_QWORD *)(qword_1435FA6E0 + 16);
  *(_DWORD *)(v14 + 40) = 130;
  a11 = qword_14393FEB8;
  v23 = *(_QWORD **)qword_1435D24B0;
  a12 = v22;
  a10 = qword_143A35618;
  *(__m128 *)&a8 = _mm_loadh_ps(qword_14393FD08);
  if ( v23 == nullptr )
  {
    v63 = (_QWORD *)qword_143A352E0(a1: *(_QWORD *)qword_1435FA560, a2: &unk_14359FC6A);
    v23 = v63;
    if ( v63 == nullptr )
    {
      qword_143A35A60(a1: 0);
      qword_143A35A30(a1: 1);
      goto LABEL_103;
    }
    ++*v63;
    *(_QWORD *)qword_1435D24B0 = v63;
  }
  v24 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64 *))unk_142F85F90)(a1, a2: v23, a3: &a8);
  v25 = (_QWORD *)v24;
  if ( v24 == 0 )
  {
    v12 = a1[12];
    v13 = a1[13];
    v21 = nullptr;
    v51 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    v52 = 130;
    a1[14] = 0;
    goto LABEL_58;
  }
  v26 = *(_QWORD *)(v24 + 8);
  if ( v26 != qword_143A355C8 && (unsigned int)qword_143A35780(a1: v26, a2: qword_143A355C8) == 0 )
  {
    v21 = (_QWORD *)qword_143A35660(a1: v25, a2: qword_14393FEC0);
    if ( v21 == nullptr )
    {
      v21 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64))unk_1430ECB60)(
                        a1,
                        a2: v25,
                        a3: qword_14393FEC0);
      goto LABEL_94;
    }
LABEL_18:
    v27 = (*v25)-- == 1;
    if ( v27 )
      (*(void (__fastcall **)(_QWORD *))(v25[1] + 48LL))(a1: v25);
    goto LABEL_20;
  }
  v21 = (_QWORD *)qword_143A35660(a1: v25, a2: qword_14393FEC0);
  if ( v21 != nullptr )
    goto LABEL_18;
  v21 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD, __int64))unk_1432AB760)(
                    a1,
                    a2: v25,
                    a3: *(_QWORD *)&qword_14393FD08[0],
                    a4: qword_14393FEC0);
LABEL_94:
  v27 = (*v25)-- == 1;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v25[1] + 48LL))(a1: v25);
  if ( v21 == nullptr )
  {
    v12 = a1[12];
    v13 = a1[13];
    v52 = 130;
    v51 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_58;
  }
LABEL_20:
  *(_DWORD *)(v14 + 40) = 132;
  v28 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, _QWORD *))unk_142F69C20)(a1, a2: v21);
  v29 = v28;
  if ( v28 == nullptr )
  {
    v12 = a1[12];
    v13 = a1[13];
    v52 = 132;
    v51 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_58;
  }
  v27 = (*v28)-- == 1;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
  v30 = ((__int64 (__fastcall *)(_QWORD *))unk_14321A480)(a1: v29);
  if ( v30 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393FE30);
    v12 = a8;
    v13 = a9;
    v52 = 133;
    v51 = a10;
    goto LABEL_58;
  }
  v31 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v30, a2: qword_14393FE60);
  v32 = v31;
  if ( v31 == nullptr )
  {
    v12 = a1[12];
    v13 = a1[13];
    v52 = 133;
    v51 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_58;
  }
  v27 = (*v31)-- == 1;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v31[1] + 48LL))(a1: v31);
  if ( v32 == (_QWORD *)qword_143A35618 )
    goto LABEL_48;
  v33 = ((__int64 (*)(void))unk_14321A480)();
  if ( v33 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393FE30);
    v12 = a8;
    v13 = a9;
    v52 = 135;
    v51 = a10;
    goto LABEL_58;
  }
  v34 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v33, a2: qword_14393FE60);
  v35 = (_QWORD *)v34;
  if ( v34 == 0 )
    goto LABEL_57;
  v36 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v34, a2: qword_14393FEC8);
  v27 = (*v35)-- == 1;
  v37 = (_QWORD *)v36;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v35[1] + 48LL))(a1: v35);
  if ( v37 == nullptr )
    goto LABEL_57;
  v38 = *(_QWORD *)(*(_QWORD *)&qword_14393FD08[0] + 32LL);
  if ( *(_BYTE *)(v38 + 10) != 0 )
  {
    v39 = *(_DWORD *)(v38 + 12);
    if ( v39 == 0 )
    {
      v39 = dword_143547A4C;
      *(_DWORD *)(v38 + 12) = dword_143547A4C++;
    }
    if ( dword_143547A40 == v39 )
    {
      v40 = qword_1439440F8;
    }
    else
    {
      dword_143547A40 = v39;
      v40 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v38,
              a2: qword_14393FED8,
              a3: *(_QWORD *)(qword_14393FED8 + 24));
      qword_1439440F8 = v40;
    }
    if ( v40 >= 0 )
    {
      v41 = v38 + (1LL << *(_BYTE *)(v38 + 9)) + 32;
      if ( *(_QWORD *)(v41 + 16 * v40 + 8) != 0 )
        goto LABEL_40;
      v75 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v38,
              a2: qword_14393FED8,
              a3: *(_QWORD *)(qword_14393FED8 + 24));
      qword_1439440F8 = v75;
      if ( v75 >= 0 )
      {
        v71 = *(_QWORD *)(v41 + 16 * v75 + 8);
LABEL_87:
        if ( v71 != 0 )
          goto LABEL_40;
      }
    }
  }
  else
  {
    v70 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)&qword_14393FD08[0], a2: qword_14393FED8);
    if ( v70 != nullptr )
    {
      v71 = *v70;
      goto LABEL_87;
    }
  }
  v72 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393FED8);
  if ( v72 == nullptr || *v72 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393FED8);
    v12 = a8;
    v13 = a9;
    v52 = 135;
    v51 = a10;
    v27 = (*v37)-- == 1;
    if ( v27 )
    {
      (*(void (__fastcall **)(_QWORD *))(v37[1] + 48LL))(a1: v37);
      v52 = 135;
    }
LABEL_58:
    if ( v51 != 0 )
    {
      if ( *(_QWORD *)(v51 + 24) != v14 )
      {
        v53 = *(_QWORD *)qword_1435FA6C0;
        if ( *(_QWORD *)qword_1435FA6C0 != 0 )
        {
          *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v53;
          *(_QWORD *)v53 = 1;
          --*(_DWORD *)qword_1435FA6D0;
        }
        else
        {
          v76 = v52;
          v73 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
          v52 = v76;
          v53 = v73;
        }
        *(_QWORD *)(v53 + 24) = v14;
        ++*(_QWORD *)v14;
        v54 = *(_QWORD *)(qword_143A35A28 + 504);
        *(_DWORD *)(v53 + 36) = v52;
        *(_DWORD *)(v53 + 32) = -1;
        v55 = *(_QWORD *)(*(_QWORD *)(v54 + 16) + 744LL);
        v56 = *(_QWORD *)(v55 + 8);
        *(_QWORD *)&v57 = v55;
        v58 = v56 | *(_QWORD *)(v53 - 8) & 3LL;
        *(_QWORD *)v56 = v53 - 16;
        *((_QWORD *)&v57 + 1) = v58;
        *(_OWORD *)(v53 - 16) = v57;
        v27 = *(_QWORD *)v51 == 0;
        *(_QWORD *)(v55 + 8) = v53 - 16;
        *(_QWORD *)(v53 + 16) = v51;
        if ( v27 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v51 + 8) + 48LL))(a1: v51);
        v51 = v53;
      }
      goto LABEL_65;
    }
    v51 = *(_QWORD *)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v51;
      *(_QWORD *)v51 = 1;
      --*(_DWORD *)qword_1435FA6D0;
LABEL_82:
      *(_QWORD *)(v51 + 16) = 0;
      *(_QWORD *)(v51 + 24) = v14;
      ++*(_QWORD *)v14;
      v64 = *(_QWORD *)(qword_143A35A28 + 504);
      *(_DWORD *)(v51 + 36) = v52;
      v65 = *(_QWORD *)(v64 + 16);
      *(_DWORD *)(v51 + 32) = -1;
      v66 = *(_QWORD *)(v65 + 744);
      v67 = *(_QWORD *)(v66 + 8);
      *(_QWORD *)&v68 = v66;
      v69 = v67 | *(_QWORD *)(v51 - 8) & 3LL;
      *(_QWORD *)v67 = v51 - 16;
      *((_QWORD *)&v68 + 1) = v69;
      *(_OWORD *)(v51 - 16) = v68;
      *(_QWORD *)(v66 + 8) = v51 - 16;
LABEL_65:
      ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v14, a2: &unk_14359FC65, a3: v21);
      if ( qword_143944108 == v14 )
      {
        v27 = (*(_QWORD *)v14)-- == 1;
        if ( v27 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v14 + 8) + 48LL))(a1: v14);
        qword_143944108 = 0;
      }
      v59 = a1[7];
      v60 = *(_QWORD *)(v59 + 8);
      v61 = *(_QWORD *)(v60 + 40);
      v62 = *(_QWORD **)(v61 + 16);
      *(_QWORD *)(v59 + 8) = *(_QWORD *)(v60 + 48);
      *(_DWORD *)(v61 + 64) = -1;
      if ( v62 != nullptr )
      {
        *(_QWORD *)(v61 + 16) = 0;
        v27 = (*v62)-- == 1;
        if ( v27 )
          (*(void (**)(void))(v62[1] + 48LL))();
      }
      v27 = (*(_QWORD *)v61)-- == 1;
      if ( v27 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v61 + 8) + 48LL))(a1: v61);
      *(_QWORD *)(v61 + 120) = 0;
      if ( v21 != nullptr )
      {
        v27 = (*v21)-- == 1;
        if ( v27 )
          (*(void (__fastcall **)(_QWORD *))(v21[1] + 48LL))(a1: v21);
      }
      MEMORY[0x13B00DF80](a1, a2: v12, a3: v13, a4: v51);
      return 0;
    }
LABEL_103:
    v77 = v52;
    v74 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
    v52 = v77;
    v51 = v74;
    goto LABEL_82;
  }
LABEL_40:
  v42 = ((__int64 (__fastcall *)(_QWORD *))unk_1432AA300)(a1: v37);
  v27 = (*v37)-- == 1;
  v43 = v42;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v37[1] + 48LL))(a1: v37);
  if ( v43 == -1 )
  {
LABEL_57:
    v51 = a1[14];
    a1[14] = 0;
    v52 = 135;
    v12 = a1[12];
    v13 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_58;
  }
  if ( v43 == 1 )
  {
    v44 = qword_143A35208;
    ++*(_QWORD *)qword_143A35208;
    goto LABEL_49;
  }
LABEL_48:
  v44 = qword_143A35200;
  ++*(_QWORD *)qword_143A35200;
LABEL_49:
  v46 = a1[7];
  v47 = *(_QWORD *)(v46 + 8);
  v48 = *(_QWORD *)(v47 + 40);
  v49 = *(_QWORD **)(v48 + 16);
  *(_QWORD *)(v46 + 8) = *(_QWORD *)(v47 + 48);
  *(_DWORD *)(v48 + 64) = -1;
  if ( v49 != nullptr )
  {
    *(_QWORD *)(v48 + 16) = 0;
    v27 = (*v49)-- == 1;
    if ( v27 )
      (*(void (**)(void))(v49[1] + 48LL))();
  }
  v27 = (*(_QWORD *)v48)-- == 1;
  if ( v27 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v48 + 8) + 48LL))(a1: v48);
  *(_QWORD *)(v48 + 120) = 0;
  v27 = (*v21)-- == 1;
  if ( v27 )
    (*(void (__fastcall **)(_QWORD *))(v21[1] + 48LL))(a1: v21);
  return v44;
}