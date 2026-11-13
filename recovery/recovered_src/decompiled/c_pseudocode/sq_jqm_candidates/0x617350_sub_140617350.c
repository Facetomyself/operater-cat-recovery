// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_140617350(_QWORD *a1, __int64 a2, _QWORD **a3, __int64 a4, __int64 a5, _QWORD *a6)
{
  __int64 v6; // rbx
  _QWORD *v7; // rbp
  __int64 v9; // rax
  __int64 v10; // rdx
  __int64 v11; // rax
  __int64 v12; // rdx
  _QWORD *v13; // rax
  _QWORD *v14; // rdi
  __int64 v15; // rdx
  __int64 v16; // rax
  bool v17; // zf
  __int64 v18; // r12
  __int64 v19; // rax
  __int64 v20; // rdx
  __int64 v21; // rbx
  _QWORD *v22; // rcx
  _QWORD *v24; // r14
  __int64 v25; // r12
  __int64 v26; // r13
  _QWORD *v27; // rdi
  __int64 v28; // rdx
  unsigned __int64 v29; // r8
  __int128 v30; // xmm0
  __int64 v31; // rax
  __int64 v32; // rax
  __int64 v33; // rdx
  __int64 v34; // rbx
  _QWORD *v35; // rcx
  __int64 v36; // rax
  __int64 v37; // rdx
  unsigned __int64 v38; // r8
  __int128 v39; // xmm0
  __int64 v40; // rax
  __int64 v41; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143943DE0;
  v7 = *a3;
  if ( qword_143943DE0 == 0 )
    goto LABEL_4;
  v9 = *(_QWORD *)qword_143943DE0;
  if ( *(__int64 *)qword_143943DE0 > 1 )
  {
    *(_QWORD *)qword_143943DE0 = v9 - 1;
LABEL_4:
    qword_143943DE0 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F08,
                        a3: qword_143943E90,
                        a4: 8);
    v6 = qword_143943DE0;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943DE0 + 16) != 0 )
  {
    v36 = v9 - 1;
    *(_QWORD *)qword_143943DE0 = v36;
    if ( v36 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943DE0 + 8) + 48LL))(a1: qword_143943DE0);
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
  v14 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v7, a2: qword_14393F6B8);
  if ( v14 != nullptr )
  {
    v15 = ((__int64 (*)(void))unk_143219690)();
    if ( v15 == 0 )
    {
      ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v41, a3: qword_14393F7B8);
      v17 = (*v14)-- == 1;
      v25 = v41;
      v26 = a5;
      v24 = a6;
      if ( v17 )
        (*(void (__fastcall **)(_QWORD *))(v14[1] + 48LL))(a1: v14);
      goto LABEL_25;
    }
    v16 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430E8490)(a1: v14, a2: v15);
    v17 = (*v14)-- == 1;
    v18 = v16;
    if ( v17 )
    {
      (*(void (__fastcall **)(_QWORD *))(v14[1] + 48LL))(a1: v14);
      if ( v18 != 0 )
      {
LABEL_15:
        v19 = a1[7];
        v20 = *(_QWORD *)(v19 + 8);
        v21 = *(_QWORD *)(v20 + 40);
        v22 = *(_QWORD **)(v21 + 16);
        *(_QWORD *)(v19 + 8) = *(_QWORD *)(v20 + 48);
        *(_DWORD *)(v21 + 64) = -1;
        if ( v22 != nullptr )
        {
          *(_QWORD *)(v21 + 16) = 0;
          v17 = (*v22)-- == 1;
          if ( v17 )
            (*(void (**)(void))(v22[1] + 48LL))();
        }
        v17 = (*(_QWORD *)v21)-- == 1;
        if ( v17 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v21 + 8) + 48LL))(a1: v21);
        *(_QWORD *)(v21 + 120) = 0;
        v17 = (*v7)-- == 1;
        if ( v17 )
          (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
        return v18;
      }
    }
    else if ( v16 != 0 )
    {
      goto LABEL_15;
    }
  }
  v24 = (_QWORD *)a1[14];
  a1[14] = 0;
  v25 = a1[12];
  v26 = a1[13];
  *((_OWORD *)a1 + 6) = 0;
LABEL_25:
  if ( v24 != nullptr )
  {
    if ( v24[3] != v6 )
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
      v27[3] = v6;
      ++*(_QWORD *)v6;
      v27[4] = qword_1435A04B0;
      v28 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v29 = *(_QWORD *)(v28 + 8);
      *(_QWORD *)&v30 = v28;
      v31 = v29 | *(v27 - 1) & 3LL;
      *(_QWORD *)v29 = v27 - 2;
      *((_QWORD *)&v30 + 1) = v31;
      *((_OWORD *)v27 - 1) = v30;
      v17 = *v24 == 0;
      *(_QWORD *)(v28 + 8) = v27 - 2;
      v27[2] = v24;
      if ( v17 )
        (*(void (__fastcall **)(_QWORD *))(v24[1] + 48LL))(a1: v24);
      v24 = v27;
    }
  }
  else
  {
    v24 = *(_QWORD **)qword_1435FA6C0;
    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
    {
      *(_QWORD *)qword_1435FA6C0 = *v24;
      *v24 = 1;
      --*(_DWORD *)qword_1435FA6D0;
    }
    else
    {
      v24 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
    }
    v24[2] = 0;
    v24[3] = v6;
    ++*(_QWORD *)v6;
    v24[4] = qword_1435A04B0;
    v37 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
    v38 = *(_QWORD *)(v37 + 8);
    *(_QWORD *)&v39 = v37;
    v40 = v38 | *(v24 - 1) & 3LL;
    *(_QWORD *)v38 = v24 - 2;
    *((_QWORD *)&v39 + 1) = v40;
    *((_OWORD *)v24 - 1) = v39;
    *(_QWORD *)(v37 + 8) = v24 - 2;
  }
  ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v6, a2: &unk_14359FC65, a3: v7);
  if ( qword_143943DE0 == v6 )
  {
    v17 = (*(_QWORD *)v6)-- == 1;
    if ( v17 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943DE0 = 0;
  }
  v32 = a1[7];
  v33 = *(_QWORD *)(v32 + 8);
  v34 = *(_QWORD *)(v33 + 40);
  v35 = *(_QWORD **)(v34 + 16);
  *(_QWORD *)(v32 + 8) = *(_QWORD *)(v33 + 48);
  *(_DWORD *)(v34 + 64) = -1;
  if ( v35 != nullptr )
  {
    *(_QWORD *)(v34 + 16) = 0;
    v17 = (*v35)-- == 1;
    if ( v17 )
      (*(void (**)(void))(v35[1] + 48LL))();
  }
  v17 = (*(_QWORD *)v34)-- == 1;
  if ( v17 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v34 + 8) + 48LL))(a1: v34);
  *(_QWORD *)(v34 + 120) = 0;
  v17 = (*v7)-- == 1;
  if ( v17 )
    (*(void (__fastcall **)(_QWORD *))(v7[1] + 48LL))(a1: v7);
  MEMORY[0x13B00DF80](a1, a2: v25, a3: v26, a4: v24);
  return 0;
}