// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_140616370(_QWORD *a1, __int64 a2, _QWORD **a3)
{
  __int64 v3; // rbx
  _QWORD *v4; // rdi
  __int64 v6; // rax
  __int64 v7; // rdx
  __int64 v8; // rax
  __int64 v9; // rdx
  _QWORD *v10; // rax
  __int64 v11; // rbp
  __int64 v12; // rax
  __int64 v13; // rdx
  __int64 v14; // rbx
  _QWORD *v15; // rcx
  bool v16; // zf
  __int64 v18; // rax
  _QWORD *v19; // r12
  __int64 v20; // r13
  __int64 v21; // r14
  _QWORD *v22; // r15
  __int64 v23; // rdx
  unsigned __int64 v24; // r8
  __int128 v25; // xmm0
  __int64 v26; // rax
  __int64 v27; // rax
  __int64 v28; // rdx
  __int64 v29; // rbx
  _QWORD *v30; // rcx
  __int64 v31; // rdx
  unsigned __int64 v32; // r8
  __int128 v33; // xmm0
  __int64 v34; // rax

  v3 = qword_143943E00;
  v4 = *a3;
  if ( qword_143943E00 == 0 )
    goto LABEL_4;
  v6 = *(_QWORD *)qword_143943E00;
  if ( *(__int64 *)qword_143943E00 > 1 )
  {
    *(_QWORD *)qword_143943E00 = v6 - 1;
LABEL_4:
    qword_143943E00 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943EE8,
                        a3: qword_143943E90,
                        a4: 8);
    v3 = qword_143943E00;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E00 + 16) != 0 )
  {
    v18 = v6 - 1;
    *(_QWORD *)qword_143943E00 = v18;
    if ( v18 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E00 + 8) + 48LL))(a1: qword_143943E00);
    goto LABEL_4;
  }
LABEL_5:
  v7 = a1[7];
  v8 = *(_QWORD *)(v7 + 8);
  *(_QWORD *)(v3 + 120) = v8;
  *(_QWORD *)(v7 + 8) = v3 + 72;
  if ( v8 != 0
    && (*(_BYTE *)(v8 + 69) == 1
     || *(_QWORD *)(v8 + 56) >= (unsigned __int64)(*(_QWORD *)(v8 + 32)
                                                 + 2LL * *(int *)(*(_QWORD *)(v8 + 32) + 168LL)
                                                 + 184)) )
  {
    v9 = *(_QWORD *)(v3 + 112);
    if ( v9 != 0 )
    {
      v10 = *(_QWORD **)(v8 + 40);
      *(_QWORD *)(v9 + 16) = v10;
      if ( v10 != nullptr )
        ++*v10;
    }
  }
  ++*(_QWORD *)v3;
  *(_DWORD *)(v3 + 64) = 0;
  v11 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v4, a2: qword_14393F700);
  if ( v11 != 0 )
  {
    v12 = a1[7];
    v13 = *(_QWORD *)(v12 + 8);
    v14 = *(_QWORD *)(v13 + 40);
    v15 = *(_QWORD **)(v14 + 16);
    *(_QWORD *)(v12 + 8) = *(_QWORD *)(v13 + 48);
    *(_DWORD *)(v14 + 64) = -1;
    if ( v15 != nullptr )
    {
      *(_QWORD *)(v14 + 16) = 0;
      v16 = (*v15)-- == 1;
      if ( v16 )
        (*(void (**)(void))(v15[1] + 48LL))();
    }
    v16 = (*(_QWORD *)v14)-- == 1;
    if ( v16 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v14 + 8) + 48LL))(a1: v14);
    *(_QWORD *)(v14 + 120) = 0;
    v16 = (*v4)-- == 1;
    if ( v16 )
      (*(void (__fastcall **)(_QWORD *))(v4[1] + 48LL))(a1: v4);
  }
  else
  {
    v19 = (_QWORD *)a1[14];
    v20 = a1[12];
    a1[14] = 0;
    v21 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
    if ( v19 != nullptr )
    {
      if ( v19[3] != v3 )
      {
        v22 = *(_QWORD **)qword_1435FA6C0;
        if ( *(_QWORD *)qword_1435FA6C0 != 0 )
        {
          *(_QWORD *)qword_1435FA6C0 = *v22;
          *v22 = 1;
          --*(_DWORD *)qword_1435FA6D0;
        }
        else
        {
          v22 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
        }
        v22[3] = v3;
        ++*(_QWORD *)v3;
        v22[4] = qword_1435A0498;
        v23 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
        v24 = *(_QWORD *)(v23 + 8);
        *(_QWORD *)&v25 = v23;
        v26 = v24 | *(v22 - 1) & 3LL;
        *(_QWORD *)v24 = v22 - 2;
        *((_QWORD *)&v25 + 1) = v26;
        *((_OWORD *)v22 - 1) = v25;
        v16 = *v19 == 0;
        *(_QWORD *)(v23 + 8) = v22 - 2;
        v22[2] = v19;
        if ( v16 )
          (*(void (__fastcall **)(_QWORD *))(v19[1] + 48LL))(a1: v19);
        v19 = v22;
      }
    }
    else
    {
      v19 = *(_QWORD **)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *v19;
        *v19 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v19 = (_QWORD *)MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      v19[3] = v3;
      v19[2] = 0;
      ++*(_QWORD *)v3;
      v19[4] = qword_1435A0498;
      v31 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v32 = *(_QWORD *)(v31 + 8);
      *(_QWORD *)&v33 = v31;
      v34 = v32 | *(v19 - 1) & 3LL;
      *(_QWORD *)v32 = v19 - 2;
      *((_QWORD *)&v33 + 1) = v34;
      *((_OWORD *)v19 - 1) = v33;
      *(_QWORD *)(v31 + 8) = v19 - 2;
    }
    ((void (__fastcall *)(__int64, void *, _QWORD *))unk_142F544C0)(a1: v3, a2: &unk_14359FC65, a3: v4);
    if ( qword_143943E00 == v3 )
    {
      v16 = (*(_QWORD *)v3)-- == 1;
      if ( v16 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v3 + 8) + 48LL))(a1: v3);
      qword_143943E00 = 0;
    }
    v27 = a1[7];
    v28 = *(_QWORD *)(v27 + 8);
    v29 = *(_QWORD *)(v28 + 40);
    v30 = *(_QWORD **)(v29 + 16);
    *(_QWORD *)(v27 + 8) = *(_QWORD *)(v28 + 48);
    *(_DWORD *)(v29 + 64) = -1;
    if ( v30 != nullptr )
    {
      *(_QWORD *)(v29 + 16) = 0;
      v16 = (*v30)-- == 1;
      if ( v16 )
        (*(void (**)(void))(v30[1] + 48LL))();
    }
    v16 = (*(_QWORD *)v29)-- == 1;
    if ( v16 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
    *(_QWORD *)(v29 + 120) = 0;
    v16 = (*v4)-- == 1;
    if ( v16 )
      (*(void (__fastcall **)(_QWORD *))(v4[1] + 48LL))(a1: v4);
    MEMORY[0x13B00DF80](a1, a2: v20, a3: v21, a4: v19);
  }
  return v11;
}