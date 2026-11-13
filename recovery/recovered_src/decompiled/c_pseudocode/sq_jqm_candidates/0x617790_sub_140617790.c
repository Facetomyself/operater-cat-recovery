// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_140617790(
        __int64 a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        _QWORD *a8)
{
  __int64 v8; // rbx
  _QWORD *v9; // rbp
  _QWORD *v10; // rdi
  __int64 v13; // rax
  __int64 v14; // rdx
  __int64 v15; // rax
  __int64 v16; // rdx
  _QWORD *v17; // rax
  __int64 v18; // rdx
  int v19; // eax
  __int64 v20; // r8
  _QWORD *v21; // r9
  __int64 v22; // rax
  _QWORD *v23; // r14
  __int64 v24; // rax
  bool v25; // zf
  __int64 v26; // r13
  __int64 v27; // rax
  __int64 v28; // rdx
  __int64 v29; // rbx
  _QWORD *v30; // rcx
  __int64 v32; // rax
  _QWORD *v33; // rdx
  __int64 (__fastcall *v34)(_QWORD *, void *); // rax
  void *v35; // rdx
  __m128i v36; // xmm0
  _QWORD *v37; // r13
  int v38; // r15d
  __m128i v39; // xmm0
  __int64 v40; // r14
  _QWORD *v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rdx
  unsigned __int64 v44; // r9
  __int128 v45; // xmm0
  __int64 v46; // rax
  __int64 v47; // rax
  __int64 v48; // rdx
  __int64 v49; // rbx
  _QWORD *v50; // rcx
  __m128i v51; // xmm0
  __int64 v52; // rax
  __int64 v53; // rax
  __int64 v54; // rdx
  unsigned __int64 v55; // r8
  __int128 v56; // xmm0
  __int64 v57; // rax
  char v58; // dl
  __int64 v59; // rdx
  __int64 v60; // rdx
  __int128 v61; // xmm0
  __int64 v62; // rax
  __int64 v63; // rax

  v8 = qword_143943DD0;
  v9 = *(_QWORD **)a3;
  v10 = *(_QWORD **)(a3 + 8);
  a8 = nullptr;
  *(_OWORD *)&a6 = 0;
  if ( qword_143943DD0 == 0 )
    goto LABEL_4;
  v13 = *(_QWORD *)qword_143943DD0;
  if ( *(__int64 *)qword_143943DD0 > 1 )
  {
    *(_QWORD *)qword_143943DD0 = v13 - 1;
LABEL_4:
    qword_143943DD0 = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F88,
                        a3: qword_143943E90,
                        a4: 24);
    v8 = qword_143943DD0;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943DD0 + 16) != 0 )
  {
    v32 = v13 - 1;
    *(_QWORD *)qword_143943DD0 = v32;
    if ( v32 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943DD0 + 8) + 48LL))(a1: qword_143943DD0);
    goto LABEL_4;
  }
LABEL_5:
  v14 = *(_QWORD *)(a1 + 56);
  v15 = *(_QWORD *)(v14 + 8);
  *(_QWORD *)(v8 + 120) = v15;
  *(_QWORD *)(v14 + 8) = v8 + 72;
  if ( v15 != 0
    && (*(_BYTE *)(v15 + 69) == 1
     || *(_QWORD *)(v15 + 56) >= (unsigned __int64)(*(_QWORD *)(v15 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v15 + 32) + 168LL)
                                                  + 184)) )
  {
    v16 = *(_QWORD *)(v8 + 112);
    if ( v16 != 0 )
    {
      v17 = *(_QWORD **)(v15 + 40);
      *(_QWORD *)(v16 + 16) = v17;
      if ( v17 != nullptr )
        ++*v17;
    }
  }
  ++*(_QWORD *)v8;
  *(_DWORD *)(v8 + 64) = 0;
  v18 = ((__int64 (*)(void))unk_143218EB0)();
  if ( v18 == 0 )
  {
    v38 = 169;
    ((void (__fastcall *)(__int64, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393F800);
    v37 = a8;
    goto LABEL_41;
  }
  v19 = qword_143A35128(a1: v10, a2: v18);
  if ( v19 == -1 )
  {
    v51 = *(__m128i *)(a1 + 96);
    v37 = *(_QWORD **)(a1 + 112);
    v38 = 169;
    *(_QWORD *)(a1 + 112) = 0;
    *(__m128i *)&a6 = v51;
    a8 = v37;
    *(_OWORD *)(a1 + 96) = 0;
    goto LABEL_41;
  }
  if ( v19 != 0 )
  {
    v33 = (_QWORD *)v10[1];
    v34 = (__int64 (__fastcall *)(_QWORD *, void *))v33[18];
    if ( v34 != nullptr )
    {
      v35 = *(void **)(qword_1435FA6E0 + 144);
    }
    else
    {
      v34 = (__int64 (__fastcall *)(_QWORD *, void *))v33[8];
      if ( v34 == nullptr )
      {
        qword_143A358D8(a1: *(_QWORD *)qword_143A353A8, a2: &unk_14359FE30, a3: v33[3]);
LABEL_37:
        v36 = *(__m128i *)(a1 + 96);
        v37 = *(_QWORD **)(a1 + 112);
        v38 = 170;
        *(_QWORD *)(a1 + 112) = 0;
        *(__m128i *)&a6 = v36;
        a8 = v37;
        *(_OWORD *)(a1 + 96) = 0;
        goto LABEL_41;
      }
      v35 = &unk_14359FE25;
    }
    v26 = v34(a1: v10, a2: v35);
    if ( v26 != 0 )
    {
LABEL_21:
      v27 = *(_QWORD *)(a1 + 56);
      v28 = *(_QWORD *)(v27 + 8);
      v29 = *(_QWORD *)(v28 + 40);
      v30 = *(_QWORD **)(v29 + 16);
      *(_QWORD *)(v27 + 8) = *(_QWORD *)(v28 + 48);
      *(_DWORD *)(v29 + 64) = -1;
      if ( v30 != nullptr )
      {
        *(_QWORD *)(v29 + 16) = 0;
        v25 = (*v30)-- == 1;
        if ( v25 )
          (*(void (**)(void))(v30[1] + 48LL))();
      }
      v25 = (*(_QWORD *)v29)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
      *(_QWORD *)(v29 + 120) = 0;
      v25 = (*v9)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
      v25 = (*v10)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v10[1] + 48LL))(a1: v10);
      return v26;
    }
    goto LABEL_37;
  }
  v20 = *(_QWORD *)(*(_QWORD *)(a2 + 216) + 16LL);
  if ( v20 != 0 )
  {
    v21 = nullptr;
    if ( v9 != (_QWORD *)qword_143A35618 )
      v21 = v9;
    v22 = ((__int64 (__fastcall *)(__int64, __int64, __int64, _QWORD *))unk_142F82550)(
            a1,
            a2: qword_14393F5F8,
            a3: v20,
            a4: v21);
    v23 = (_QWORD *)v22;
    if ( v22 != 0 )
    {
      *(_DWORD *)(v8 + 40) = 171;
      v24 = ((__int64 (__fastcall *)(__int64, __int64, __int64, _QWORD *))unk_1430D9050)(
              a1,
              a2: v22,
              a3: qword_14393F810,
              a4: v10);
      v25 = (*v23)-- == 1;
      v26 = v24;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v23[1] + 48LL))(a1: v23);
      if ( v26 != 0 )
        goto LABEL_21;
    }
    v37 = *(_QWORD **)(a1 + 112);
    v39 = *(__m128i *)(a1 + 96);
    v38 = 171;
    *(_QWORD *)(a1 + 112) = 0;
    a8 = v37;
    *(__m128i *)&a6 = v39;
    *(_OWORD *)(a1 + 96) = 0;
  }
  else
  {
    v58 = *(_BYTE *)(qword_14393F808 + 32);
    if ( (v58 & 0x40) == 0 || (v25 = (v58 & 0x20) == 0, v59 = qword_14393F808 + 48, v25) )
      v59 = *(_QWORD *)(qword_14393F808 + 56);
    v60 = qword_143A35810(a1: &unk_14359FC00, a2: v59);
    *(_QWORD *)&v61 = *(_QWORD *)qword_143A35458;
    ++*(_QWORD *)v61;
    a8 = nullptr;
    *((_QWORD *)&v61 + 1) = v60;
    *(_OWORD *)&a6 = v61;
    if ( (_QWORD)v61 != qword_143A35618 )
    {
      ((void (__fastcall *)(__int64, __int64 *, __int64 *, _QWORD **))unk_142FAD280)(a1, a2: &a6, a3: &a7, a4: &a8);
      v60 = a7;
    }
    v38 = 171;
    ((void (__fastcall *)(_QWORD, __int64))unk_143526380)(a1: *(_QWORD *)(a1 + 312), a2: v60);
    v37 = a8;
  }
LABEL_41:
  if ( v37 == nullptr )
  {
    v40 = *(_QWORD *)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v40;
      *(_QWORD *)v40 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v63 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
      v37 = a8;
      v40 = v63;
    }
    *(_QWORD *)(v40 + 16) = 0;
    *(_QWORD *)(v40 + 24) = v8;
    ++*(_QWORD *)v8;
    v52 = *(_QWORD *)(qword_143A35A28 + 504);
    *(_DWORD *)(v40 + 32) = -1;
    v53 = *(_QWORD *)(v52 + 16);
    *(_DWORD *)(v40 + 36) = v38;
    v54 = *(_QWORD *)(v53 + 744);
    v55 = *(_QWORD *)(v54 + 8);
    *(_QWORD *)&v56 = v54;
    v57 = v55 | *(_QWORD *)(v40 - 8) & 3LL;
    *(_QWORD *)v55 = v40 - 16;
    *((_QWORD *)&v56 + 1) = v57;
    *(_OWORD *)(v40 - 16) = v56;
    *(_QWORD *)(v54 + 8) = v40 - 16;
    if ( v37 != nullptr )
    {
      v25 = (*v37)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v37[1] + 48LL))(a1: v37);
    }
    goto LABEL_48;
  }
  if ( v37[3] != v8 )
  {
    v40 = *(_QWORD *)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      v41 = v37;
      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v40;
      *(_QWORD *)v40 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v62 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
      v41 = a8;
      v40 = v62;
    }
    *(_QWORD *)(v40 + 24) = v8;
    ++*(_QWORD *)v8;
    v42 = *(_QWORD *)(qword_143A35A28 + 504);
    *(_DWORD *)(v40 + 32) = -1;
    *(_DWORD *)(v40 + 36) = v38;
    v43 = *(_QWORD *)(*(_QWORD *)(v42 + 16) + 744LL);
    v44 = *(_QWORD *)(v43 + 8);
    *(_QWORD *)&v45 = v43;
    v46 = v44 | *(_QWORD *)(v40 - 8) & 3LL;
    *(_QWORD *)v44 = v40 - 16;
    *((_QWORD *)&v45 + 1) = v46;
    *(_OWORD *)(v40 - 16) = v45;
    *(_QWORD *)(v43 + 8) = v40 - 16;
    *(_QWORD *)(v40 + 16) = v37;
    ++*v37;
    if ( v41 != nullptr )
    {
      v25 = (*v41)-- == 1;
      if ( v25 )
        (*(void (**)(void))(v41[1] + 48LL))();
    }
LABEL_48:
    a8 = (_QWORD *)v40;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *, _QWORD *))unk_142F544C0)(a1: v8, a2: &unk_14359FC61, a3: v9, a4: v10);
  if ( qword_143943DD0 == v8 )
  {
    v25 = (*(_QWORD *)v8)-- == 1;
    if ( v25 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v8 + 8) + 48LL))(a1: v8);
    qword_143943DD0 = 0;
  }
  v47 = *(_QWORD *)(a1 + 56);
  v48 = *(_QWORD *)(v47 + 8);
  v49 = *(_QWORD *)(v48 + 40);
  v50 = *(_QWORD **)(v49 + 16);
  *(_QWORD *)(v47 + 8) = *(_QWORD *)(v48 + 48);
  *(_DWORD *)(v49 + 64) = -1;
  if ( v50 != nullptr )
  {
    *(_QWORD *)(v49 + 16) = 0;
    v25 = (*v50)-- == 1;
    if ( v25 )
      (*(void (**)(void))(v50[1] + 48LL))();
  }
  v25 = (*(_QWORD *)v49)-- == 1;
  if ( v25 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v49 + 8) + 48LL))(a1: v49);
  *(_QWORD *)(v49 + 120) = 0;
  v25 = (*v9)-- == 1;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
  v25 = (*v10)-- == 1;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v10[1] + 48LL))(a1: v10);
  v26 = 0;
  MEMORY[0x13B00DF80](a1, a2: a6, a3: a7, a4: a8);
  return v26;
}