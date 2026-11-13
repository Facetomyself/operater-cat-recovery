// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406CC6B0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6)
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
  __int64 v17; // rax
  _QWORD *v18; // rdi
  int v19; // ebp
  __int64 v20; // rdx
  __int64 v21; // rdi
  __int64 v22; // rax
  __int64 v23; // rdx
  __int64 v24; // rbx
  _QWORD *v25; // rcx
  bool v26; // zf
  _QWORD *v28; // rax
  int v29; // r14d
  __int64 v30; // r12
  __int64 v31; // r13
  __int64 v32; // rbp
  __int64 v33; // rdi
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
  __int64 v44; // rdx
  __int64 *v45; // rax
  __int64 v46; // rdx
  __int64 v47; // rax
  __int64 v48; // rax
  __int64 v49; // rdx
  unsigned __int64 v50; // r8
  __int128 v51; // xmm0
  __int64 v52; // rax
  __int64 v53; // rax
  __int64 v54; // [rsp+98h] [rbp+20h] BYREF

  v6 = qword_143943D78;
  if ( qword_143943D78 == 0 )
    goto LABEL_4;
  v8 = *(_QWORD *)qword_143943D78;
  if ( *(__int64 *)qword_143943D78 > 1 )
  {
    *(_QWORD *)qword_143943D78 = v8 - 1;
LABEL_4:
    qword_143943D78 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, _QWORD))unk_142F58E90)(
                        a1,
                        a2: qword_143943EF0,
                        a3: qword_143943E90,
                        a4: 0);
    v6 = qword_143943D78;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943D78 + 16) != 0 )
  {
    v43 = v8 - 1;
    *(_QWORD *)qword_143943D78 = v43;
    if ( v43 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943D78 + 8) + 48LL))(a1: qword_143943D78);
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
    if ( dword_143547A08 == v14 )
    {
      v15 = qword_143943D70;
      if ( qword_143943D70 < 0 )
        goto LABEL_31;
    }
    else
    {
      dword_143547A08 = v14;
      v15 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v13,
              a2: qword_14393F950,
              a3: *(_QWORD *)(qword_14393F950 + 24));
      qword_143943D70 = v15;
      if ( v15 < 0 )
        goto LABEL_31;
    }
    v16 = v13 + (1LL << *(_BYTE *)(v13 + 9)) + 32;
    if ( *(_QWORD *)(v16 + 16 * v15 + 8) != 0 )
      goto LABEL_17;
    v53 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v13,
            a2: qword_14393F950,
            a3: *(_QWORD *)(qword_14393F950 + 24));
    qword_143943D70 = v53;
    if ( v53 >= 0 )
    {
      v46 = *(_QWORD *)(v16 + 16 * v53 + 8);
LABEL_60:
      if ( v46 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v45 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F950);
    if ( v45 != nullptr )
    {
      v46 = *v45;
      goto LABEL_60;
    }
  }
LABEL_31:
  v28 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F950);
  if ( v28 == nullptr || *v28 == 0 )
  {
    v29 = 300;
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v54, a3: qword_14393F950);
    v30 = v54;
    v31 = a5;
    v32 = a6;
    goto LABEL_34;
  }
LABEL_17:
  *(_DWORD *)(v6 + 40) = 300;
  v17 = ((__int64 (__fastcall *)(_QWORD *))unk_142F69C20)(a1);
  v18 = (_QWORD *)v17;
  if ( v17 != 0 )
  {
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
      if ( v20 == 0 )
        (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
      v29 = 300;
    }
    else
    {
      *v18 = v20;
      if ( v20 == 0 )
        (*(void (__fastcall **)(_QWORD *))(v18[1] + 48LL))(a1: v18);
      if ( v19 == 0 )
      {
        v21 = qword_143A35208;
        ++*(_QWORD *)qword_143A35208;
        goto LABEL_23;
      }
      v44 = ((__int64 (*)(void))unk_143218D60)();
      if ( v44 != 0 )
      {
        *(_DWORD *)(v6 + 40) = 301;
        v21 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_1430D8EF0)(a1, a2: v44, a3: qword_14393F958);
        if ( v21 != 0 )
        {
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
          return v21;
        }
        v30 = a1[12];
        v31 = a1[13];
        v29 = 301;
        v32 = a1[14];
        *((_OWORD *)a1 + 6) = 0;
        a1[14] = 0;
      }
      else
      {
        v29 = 301;
        ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &v54, a3: qword_14393F948);
        v30 = v54;
        v31 = a5;
        v32 = a6;
      }
    }
  }
  else
  {
    v30 = a1[12];
    v31 = a1[13];
    v29 = 300;
    v32 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
  }
LABEL_34:
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
    v47 = *(_QWORD *)(qword_143A35A28 + 504);
    *(_DWORD *)(v32 + 32) = -1;
    v48 = *(_QWORD *)(v47 + 16);
    *(_DWORD *)(v32 + 36) = v29;
    v49 = *(_QWORD *)(v48 + 744);
    v50 = *(_QWORD *)(v49 + 8);
    *(_QWORD *)&v51 = v49;
    v52 = v50 | *(_QWORD *)(v32 - 8) & 3LL;
    *(_QWORD *)v50 = v32 - 16;
    *((_QWORD *)&v51 + 1) = v52;
    *(_OWORD *)(v32 - 16) = v51;
    *(_QWORD *)(v49 + 8) = v32 - 16;
  }
  ((void (__fastcall *)(__int64, _QWORD))unk_142F544C0)(a1: v6, a2: 0);
  if ( qword_143943D78 == v6 )
  {
    v26 = (*(_QWORD *)v6)-- == 1;
    if ( v26 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v6 + 8) + 48LL))(a1: v6);
    qword_143943D78 = 0;
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
  v21 = 0;
  MEMORY[0x13B00DF80](a1, a2: v30, a3: v31, a4: v32);
  return v21;
}