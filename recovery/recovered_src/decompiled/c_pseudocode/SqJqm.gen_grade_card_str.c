// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_140615E30(_QWORD *a1, __int64 a2, _QWORD **a3, __int64 a4, __int64 a5, _QWORD *a6)
{
  __int64 v6; // rbx
  _QWORD *v7; // rbp
  __int64 v9; // rax
  __int64 v10; // rdx
  __int64 v11; // rax
  __int64 v12; // rdx
  _QWORD *v13; // rax
  __int64 v14; // rcx
  _QWORD *v15; // rdi
  _QWORD *v16; // r12
  __int64 v17; // rax
  _QWORD *v18; // r13
  __int64 v19; // rax
  bool v20; // zf
  __int64 v21; // r14
  __int64 v22; // rax
  __int64 v23; // rdx
  __int64 v24; // rbx
  _QWORD *v25; // rcx
  __int64 v27; // rax
  _QWORD *v28; // r15
  _QWORD *v29; // r13
  __int64 v30; // r14
  _QWORD *v31; // rdi
  __int64 v32; // rdx
  unsigned __int64 v33; // r8
  __int128 v34; // xmm0
  __int64 v35; // rax
  __int64 v36; // rax
  __int64 v37; // rdx
  __int64 v38; // rbx
  _QWORD *v39; // rcx
  __int64 v40; // rdx
  unsigned __int64 v41; // r8
  __int128 v42; // xmm0
  __int64 v43; // rax
  _QWORD *v44; // [rsp+A8h] [rbp+20h] BYREF

  v6 = qword_143943E08;
  v7 = *a3;
  if ( qword_143943E08 == 0 )
    goto LABEL_4;
  v9 = *(_QWORD *)qword_143943E08;
  if ( *(__int64 *)qword_143943E08 > 1 )
  {
    *(_QWORD *)qword_143943E08 = v9 - 1;
LABEL_4:
    qword_143943E08 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F70,
                        a3: qword_143943E90,
                        a4: 8);
    v6 = qword_143943E08;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E08 + 16) != 0 )
  {
    v27 = v9 - 1;
    *(_QWORD *)qword_143943E08 = v27;
    if ( v27 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E08 + 8) + 48LL))(a1: qword_143943E08);
    goto LABEL_4;
  }
LABEL_5:
  v10 = a1[7];
  v11 = *(_QWORD *)(v10 + 8);
  *(_QWORD *)(v6 + 120) = v11;
  *(_QWORD *)(v10 + 8) = v6 + 72;
  if ( v11 != 0
    && (*(_BYTE *)(v11 + 69) == 1
     || *(_QWORD *)(v11 + 56) >= (unsigned __int64)(*(_QWORD *)(v11 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v11 + 32) + 168LL)
                                                  + 184)) )
  {
    v12 = *(_QWORD *)(v6 + 112);
    if ( v12 != 0 )
    {
      v13 = *(_QWORD **)(v11 + 40);
      *(_QWORD *)(v12 + 16) = v13;
      if ( v13 != nullptr )
        ++*v13;
    }
  }
  ++*(_QWORD *)v6;
  *(_DWORD *)(v6 + 64) = 0;
  v14 = ((__int64 (*)(void))unk_143219FA0)();
  if ( v14 != 0 )
  {
    v15 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F7B0);
    if ( v15 != nullptr )
    {
      v16 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v7, a2: qword_14393F658);
      if ( v16 == nullptr )
      {
        v29 = (_QWORD *)a1[12];
        v30 = a1[13];
        v28 = (_QWORD *)a1[14];
        *((_OWORD *)a1 + 6) = 0;
        a1[14] = 0;
        v20 = (*v15)-- == 1;
        if ( v20 )
          (*(void (__fastcall **)(_QWORD *))(v15[1] + 48LL))(a1: v15);
        goto LABEL_34;
      }
      v17 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v7, a2: qword_14393F660);
      v18 = (_QWORD *)v17;
      if ( v17 == 0 )
      {
        v29 = (_QWORD *)a1[12];
        v30 = a1[13];
        v28 = (_QWORD *)a1[14];
        *((_OWORD *)a1 + 6) = 0;
        a1[14] = 0;
        v20 = (*v15)-- == 1;
        if ( v20 )
          (*(void (__fastcall **)(_QWORD *))(v15[1] + 48LL))(a1: v15);
        v20 = (*v16)-- == 1;
        if ( v20 )
          (*(void (__fastcall **)(_QWORD *))(v16[1] + 48LL))(a1: v16);
        goto LABEL_34;
      }
      *(_DWORD *)(v6 + 40) = 136;
      v44 = v16;
      a5 = v17;
      v19 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **))unk_142F79F60)(a1, a2: v15, a3: &v44);
      v20 = (*v15)-- == 1;
      v21 = v19;
      if ( v20 )
        (*(void (__fastcall **)(_QWORD *))(v15[1] + 48LL))(a1: v15);
      v20 = (*v16)-- == 1;
      if ( v20 )
        (*(void (__fastcall **)(_QWORD *))(v16[1] + 48LL))(a1: v16);
      v20 = (*v18)-- == 1;
      if ( v20 )
        (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
      if ( v21 != 0 )
      {
        v22 = a1[7];
        v23 = *(_QWORD *)(v22 + 8);
        v24 = *(_QWORD *)(v23 + 40);
        v25 = *(_QWORD **)(v24 + 16);
        *(_QWORD *)(v22 + 8) = *(_QWORD *)(v23 + 48);
        *(_DWORD *)(v24 + 64) = -1;
        if ( v25 != nullptr )
        {
          *(_QWORD *)(v24 + 16) = 0;
          v20 = (*v25)-- == 1;
          if ( v20 )
            (*(void (**)(void))(v25[1] + 48LL))();
        }
        v20 = (*(_QWORD *)v24)-- == 1;
        if ( v20 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v24 + 8) + 48LL))(a1: v24);
        *(_QWORD *)(v24 + 120) = 0;
        v20 = (*v7)-- == 1;
        if ( v20 )
          (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
        return v21;
      }
    }
    v28 = (_QWORD *)a1[14];
    a1[14] = 0;
    v29 = (_QWORD *)a1[12];
    v30 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
  }
  else
  {
    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &v44, a3: qword_14393F638);
    v29 = v44;
    v30 = a5;
    v28 = a6;
  }
LABEL_34:
  if ( v28 != nullptr )
  {
    if ( v28[3] != v6 )
    {
      v31 = *(_QWORD **)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *v31;
        *v31 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v31 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      v31[3] = v6;
      ++*(_QWORD *)v6;
      v31[4] = qword_1435A0490;
      v32 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v33 = *(_QWORD *)(v32 + 8);
      *(_QWORD *)&v34 = v32;
      v35 = v33 | *(v31 - 1) & 3LL;
      *(_QWORD *)v33 = v31 - 2;
      *((_QWORD *)&v34 + 1) = v35;
      *((_OWORD *)v31 - 1) = v34;
      v20 = *v28 == 0;
      *(_QWORD *)(v32 + 8) = v31 - 2;
      v31[2] = v28;
      if ( v20 )
        (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
      v28 = v31;
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
    v28[4] = qword_1435A0490;
    v40 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v41 = *(_QWORD *)(v40 + 8);
    *(_QWORD *)&v42 = v40;
    v43 = v41 | *(v28 - 1) & 3LL;
    *(_QWORD *)v41 = v28 - 2;
    *((_QWORD *)&v42 + 1) = v43;
    *((_OWORD *)v28 - 1) = v42;
    *(_QWORD *)(v40 + 8) = v28 - 2;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v6, a2: &unk_14359FC65, a3: v7);
  if ( qword_143943E08 == v6 )
  {
    v20 = (*(_QWORD *)v6)-- == 1;
    if ( v20 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943E08 = 0;
  }
  v36 = a1[7];
  v37 = *(_QWORD *)(v36 + 8);
  v38 = *(_QWORD *)(v37 + 40);
  v39 = *(_QWORD **)(v38 + 16);
  *(_QWORD *)(v36 + 8) = *(_QWORD *)(v37 + 48);
  *(_DWORD *)(v38 + 64) = -1;
  if ( v39 != nullptr )
  {
    *(_QWORD *)(v38 + 16) = 0;
    v20 = (*v39)-- == 1;
    if ( v20 )
      (*(void (**)(void))(v39[1] + 48LL))();
  }
  v20 = (*(_QWORD *)v38)-- == 1;
  if ( v20 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v38 + 8) + 48LL))(a1: v38);
  *(_QWORD *)(v38 + 120) = 0;
  v20 = (*v7)-- == 1;
  if ( v20 )
    (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
  MEMORY[0x13B00DF80](a1, a2: v29, a3: v30, a4: v28);
  return 0;
}