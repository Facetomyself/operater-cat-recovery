// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_140615990(_QWORD *a1, __int64 a2, _QWORD **a3, __int64 a4, __int64 a5, _QWORD *a6)
{
  __int64 v6; // rbx
  _QWORD *v7; // r12
  __int64 v9; // rax
  __int64 v10; // rdx
  __int64 v11; // rax
  __int64 v12; // rdx
  _QWORD *v13; // rax
  __int64 v14; // rcx
  _QWORD *v15; // rdi
  __int64 v16; // rax
  _QWORD *v17; // rbp
  __int64 v18; // rax
  bool v19; // zf
  __int64 v20; // r13
  __int64 v21; // rax
  __int64 v22; // rdx
  __int64 v23; // rbx
  _QWORD *v24; // rcx
  __int64 v26; // rax
  _QWORD *v27; // rbp
  __int64 v28; // r13
  __int64 v29; // r14
  _QWORD *v30; // rdi
  __int64 v31; // rdx
  unsigned __int64 v32; // r8
  __int128 v33; // xmm0
  __int64 v34; // rax
  __int64 v35; // rax
  __int64 v36; // rdx
  __int64 v37; // rbx
  _QWORD *v38; // rcx
  __int64 v39; // rdx
  unsigned __int64 v40; // r8
  __int128 v41; // xmm0
  __int64 v42; // rax
  __int64 v43; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143943E10;
  v7 = *a3;
  if ( qword_143943E10 == 0 )
    goto LABEL_4;
  v9 = *(_QWORD *)qword_143943E10;
  if ( *(__int64 *)qword_143943E10 > 1 )
  {
    *(_QWORD *)qword_143943E10 = v9 - 1;
LABEL_4:
    qword_143943E10 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F78,
                        a3: qword_143943E90,
                        a4: 8);
    v6 = qword_143943E10;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E10 + 16) != 0 )
  {
    v26 = v9 - 1;
    *(_QWORD *)qword_143943E10 = v26;
    if ( v26 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E10 + 8) + 48LL))(a1: qword_143943E10);
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
    v15 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F770);
    if ( v15 != nullptr )
    {
      v16 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v7, a2: qword_14393F660);
      v17 = (_QWORD *)v16;
      if ( v16 == 0 )
      {
        v28 = a1[12];
        v29 = a1[13];
        v27 = (_QWORD *)a1[14];
        *((_OWORD *)a1 + 6) = 0;
        a1[14] = 0;
        v19 = (*v15)-- == 1;
        if ( v19 )
          (*(void (__fastcall **)(_QWORD *))(v15[1] + 48LL))(a1: v15);
        goto LABEL_31;
      }
      *(_DWORD *)(v6 + 40) = 133;
      v18 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64))unk_142F6A9F0)(a1, a2: v15, a3: v16);
      v19 = (*v15)-- == 1;
      v20 = v18;
      if ( v19 )
        (*(void (__fastcall **)(_QWORD *))(v15[1] + 48LL))(a1: v15);
      v19 = (*v17)-- == 1;
      if ( v19 )
        (*(void (__fastcall **)(_QWORD *))(v17[1] + 48LL))(a1: v17);
      if ( v20 != 0 )
      {
        v21 = a1[7];
        v22 = *(_QWORD *)(v21 + 8);
        v23 = *(_QWORD *)(v22 + 40);
        v24 = *(_QWORD **)(v23 + 16);
        *(_QWORD *)(v21 + 8) = *(_QWORD *)(v22 + 48);
        *(_DWORD *)(v23 + 64) = -1;
        if ( v24 != nullptr )
        {
          *(_QWORD *)(v23 + 16) = 0;
          v19 = (*v24)-- == 1;
          if ( v19 )
            (*(void (**)(void))(v24[1] + 48LL))();
        }
        v19 = (*(_QWORD *)v23)-- == 1;
        if ( v19 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v23 + 8) + 48LL))(a1: v23);
        *(_QWORD *)(v23 + 120) = 0;
        v19 = (*v7)-- == 1;
        if ( v19 )
          (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
        return v20;
      }
    }
    v27 = (_QWORD *)a1[14];
    a1[14] = 0;
    v28 = a1[12];
    v29 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
  }
  else
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v43, a3: qword_14393F638);
    v28 = v43;
    v29 = a5;
    v27 = a6;
  }
LABEL_31:
  if ( v27 != nullptr )
  {
    if ( v27[3] != v6 )
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
      v30[4] = qword_1435A0488;
      v31 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v32 = *(_QWORD *)(v31 + 8);
      *(_QWORD *)&v33 = v31;
      v34 = v32 | *(v30 - 1) & 3LL;
      *(_QWORD *)v32 = v30 - 2;
      *((_QWORD *)&v33 + 1) = v34;
      *((_OWORD *)v30 - 1) = v33;
      v19 = *v27 == 0;
      *(_QWORD *)(v31 + 8) = v30 - 2;
      v30[2] = v27;
      if ( v19 )
        (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
      v27 = v30;
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
    v27[4] = qword_1435A0488;
    v39 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v40 = *(_QWORD *)(v39 + 8);
    *(_QWORD *)&v41 = v39;
    v42 = v40 | *(v27 - 1) & 3LL;
    *(_QWORD *)v40 = v27 - 2;
    *((_QWORD *)&v41 + 1) = v42;
    *((_OWORD *)v27 - 1) = v41;
    *(_QWORD *)(v39 + 8) = v27 - 2;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v6, a2: &unk_14359FC65, a3: v7);
  if ( qword_143943E10 == v6 )
  {
    v19 = (*(_QWORD *)v6)-- == 1;
    if ( v19 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943E10 = 0;
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
    v19 = (*v38)-- == 1;
    if ( v19 )
      (*(void (**)(void))(v38[1] + 48LL))();
  }
  v19 = (*(_QWORD *)v37)-- == 1;
  if ( v19 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v37 + 8) + 48LL))(a1: v37);
  *(_QWORD *)(v37 + 120) = 0;
  v19 = (*v7)-- == 1;
  if ( v19 )
    (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
  MEMORY[0x13B00DF80](a1, a2: v28, a3: v29, a4: v27);
  return 0;
}