// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406BC4E0(
        _QWORD *a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8)
{
  __int64 v8; // rbx
  _QWORD *v9; // r12
  _QWORD *v10; // rbp
  __int64 v12; // rax
  __int64 v13; // rdx
  __int64 v14; // rax
  __int64 v15; // rdx
  _QWORD *v16; // rax
  __int64 v17; // rdi
  int v18; // eax
  __int64 v19; // rax
  __int64 v20; // r13
  __int64 v21; // rdx
  __int64 v22; // rax
  _QWORD *v23; // rdi
  int v24; // eax
  bool v25; // zf
  int v26; // r13d
  __int64 v27; // rax
  _QWORD *v28; // rdi
  int v29; // eax
  int v30; // r13d
  __int64 v31; // rdi
  __int64 v32; // rax
  __int64 v33; // rdx
  __int64 v34; // rbx
  _QWORD *v35; // rcx
  __int64 *v37; // rax
  __int64 v38; // rdi
  __int64 v39; // r13
  int v40; // edx
  __int64 v41; // r14
  __int64 v42; // rax
  __int64 v43; // rax
  __int64 v44; // rdx
  unsigned __int64 v45; // r8
  __int128 v46; // xmm0
  __int64 v47; // rax
  __int64 v48; // rax
  __int64 v49; // r15
  __int64 v50; // rax
  __int64 v51; // rdx
  unsigned __int64 v52; // r8
  __int128 v53; // xmm0
  __int64 v54; // rax
  __int64 v55; // rax
  __int64 v56; // rdx
  __int64 v57; // rbx
  _QWORD *v58; // rcx
  __int64 v59; // r13
  __int64 v60; // rax
  _QWORD *v61; // rdi
  __int64 v62; // rax
  _QWORD *v63; // r13
  __int64 *v64; // rax
  __int64 v65; // rax
  __int64 v66; // rax
  __int64 v67; // rax
  int v68; // [rsp+C4h] [rbp+2Ch]
  int v69; // [rsp+C4h] [rbp+2Ch]

  v8 = qword_143944168;
  v9 = *(_QWORD **)a3;
  v10 = *(_QWORD **)(a3 + 8);
  if ( qword_143944168 == 0 )
    goto LABEL_4;
  v12 = *(_QWORD *)qword_143944168;
  if ( *(__int64 *)qword_143944168 > 1 )
  {
    *(_QWORD *)qword_143944168 = v12 - 1;
LABEL_4:
    qword_143944168 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143944158,
                        a3: qword_143944160,
                        a4: 16);
    v8 = qword_143944168;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143944168 + 16) != 0 )
  {
    v48 = v12 - 1;
    *(_QWORD *)qword_143944168 = v48;
    if ( v48 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143944168 + 8) + 48LL))(a1: qword_143944168);
    goto LABEL_4;
  }
LABEL_5:
  v13 = a1[7];
  v14 = *(_QWORD *)(v13 + 8);
  *(_QWORD *)(v8 + 120) = v14;
  *(_QWORD *)(v13 + 8) = v8 + 72;
  if ( v14 != 0
    && (*(_BYTE *)(v14 + 69) == 1
     || *(_QWORD *)(v14 + 56) >= (unsigned __int64)(*(_QWORD *)(v14 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v14 + 32) + 168LL)
                                                  + 184)) )
  {
    v15 = *(_QWORD *)(v8 + 112);
    if ( v15 != 0 )
    {
      v16 = *(_QWORD **)(v14 + 40);
      *(_QWORD *)(v15 + 16) = v16;
      if ( v16 != nullptr )
        ++*v16;
    }
  }
  ++*(_QWORD *)v8;
  *(_DWORD *)(v8 + 64) = 0;
  v17 = *(_QWORD *)(qword_14393FD08 + 32);
  if ( *(_BYTE *)(v17 + 10) != 0 )
  {
    v18 = *(_DWORD *)(v17 + 12);
    if ( v18 == 0 )
    {
      v18 = dword_143547A4C;
      *(_DWORD *)(v17 + 12) = dword_143547A4C++;
    }
    if ( dword_143547A50 == v18 )
    {
      v19 = qword_143944150;
      if ( qword_143944150 < 0 )
        goto LABEL_38;
    }
    else
    {
      dword_143547A50 = v18;
      v19 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v17,
              a2: qword_14393FD20,
              a3: *(_QWORD *)(qword_14393FD20 + 24));
      qword_143944150 = v19;
      if ( v19 < 0 )
        goto LABEL_38;
    }
    v20 = v17 + (1LL << *(_BYTE *)(v17 + 9)) + 32;
    v21 = *(_QWORD *)(v20 + 16 * v19 + 8);
    if ( v21 != 0 )
      goto LABEL_17;
    v65 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v17,
            a2: qword_14393FD20,
            a3: *(_QWORD *)(qword_14393FD20 + 24));
    qword_143944150 = v65;
    if ( v65 >= 0 )
    {
      v21 = *(_QWORD *)(v20 + 16 * v65 + 8);
LABEL_79:
      if ( v21 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v64 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393FD08, a2: qword_14393FD20);
    if ( v64 != nullptr )
    {
      v21 = *v64;
      goto LABEL_79;
    }
  }
LABEL_38:
  v37 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393FD20);
  if ( v37 == nullptr || (v21 = *v37, *v37 == 0) )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393FD20);
    v38 = a8;
    v39 = a6;
    v40 = 13;
    v41 = a7;
    if ( a8 != 0 )
      goto LABEL_49;
    goto LABEL_41;
  }
LABEL_17:
  *(_DWORD *)(v8 + 40) = 13;
  v22 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_1430D8EF0)(a1, a2: v21, a3: qword_14393FD28);
  v23 = (_QWORD *)v22;
  if ( v22 != 0 )
  {
    v24 = MEMORY[0x13B01B050](a1: v22);
    v25 = (*v23)-- == 1;
    v26 = v24;
    if ( v25 )
      (*(void (__fastcall **)(_QWORD *))(v23[1] + 48LL))(a1: v23);
    if ( v26 != -1 )
    {
      v27 = MEMORY[0x13B054620](a1, a2: v10, a3: qword_14393FD30);
      v28 = (_QWORD *)v27;
      if ( v27 != 0 )
      {
        v29 = MEMORY[0x13B01B050](a1: v27);
        v25 = (*v28)-- == 1;
        v30 = v29;
        if ( v25 )
          (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
        if ( v30 != -1 )
        {
          if ( v30 == 0 )
          {
            v59 = MEMORY[0x13B135D60](a1: qword_14393FD38);
            v60 = MEMORY[0x13B054620](a1, a2: v10, a3: qword_14393FD40);
            v61 = (_QWORD *)v60;
            if ( v60 == 0 )
              goto LABEL_84;
            *(_DWORD *)(v8 + 40) = 17;
            v62 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F6A9F0)(a1, a2: v59, a3: v60);
            v25 = (*v61)-- == 1;
            v63 = (_QWORD *)v62;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v61[1] + 48LL))(a1: v61);
            if ( v63 == nullptr )
            {
LABEL_84:
              v39 = a1[12];
              v41 = a1[13];
              v40 = 17;
              v38 = a1[14];
              *((_OWORD *)a1 + 6) = 0;
              a1[14] = 0;
              goto LABEL_48;
            }
            v25 = (*v63)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v63[1] + 48LL))(a1: v63);
          }
          v31 = MEMORY[0x13B054620](a1, a2: v10, a3: qword_14393FD30);
          if ( v31 != 0 )
          {
            v32 = a1[7];
            v33 = *(_QWORD *)(v32 + 8);
            v34 = *(_QWORD *)(v33 + 40);
            v35 = *(_QWORD **)(v34 + 16);
            *(_QWORD *)(v32 + 8) = *(_QWORD *)(v33 + 48);
            *(_DWORD *)(v34 + 64) = -1;
            if ( v35 != nullptr )
            {
              *(_QWORD *)(v34 + 16) = 0;
              v25 = (*v35)-- == 1;
              if ( v25 )
                (*(void (**)(void))(v35[1] + 48LL))();
            }
            v25 = (*(_QWORD *)v34)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v34 + 8) + 48LL))(a1: v34);
            *(_QWORD *)(v34 + 120) = 0;
            v25 = (*v9)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
            v25 = (*v10)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v10[1] + 48LL))(a1: v10);
            return v31;
          }
          v39 = a1[12];
          v41 = a1[13];
          v40 = 18;
          v38 = a1[14];
          *((_OWORD *)a1 + 6) = 0;
          a1[14] = 0;
LABEL_48:
          if ( v38 != 0 )
          {
LABEL_49:
            if ( *(_QWORD *)(v38 + 24) != v8 )
            {
              v49 = *(_QWORD *)qword_1435FA6C0;
              if ( *(_QWORD *)qword_1435FA6C0 != 0 )
              {
                *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v49;
                *(_QWORD *)v49 = 1;
                --*(_DWORD *)qword_1435FA6D0;
              }
              else
              {
                v68 = v40;
                v66 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                v40 = v68;
                v49 = v66;
              }
              *(_QWORD *)(v49 + 24) = v8;
              ++*(_QWORD *)v8;
              v50 = *(_QWORD *)(qword_143A35A28 + 504);
              *(_DWORD *)(v49 + 36) = v40;
              *(_DWORD *)(v49 + 32) = -1;
              v51 = *(_QWORD *)(*(_QWORD *)(v50 + 16) + 744LL);
              v52 = *(_QWORD *)(v51 + 8);
              *(_QWORD *)&v53 = v51;
              v54 = v52 | *(_QWORD *)(v49 - 8) & 3LL;
              *(_QWORD *)v52 = v49 - 16;
              *((_QWORD *)&v53 + 1) = v54;
              *(_OWORD *)(v49 - 16) = v53;
              v25 = *(_QWORD *)v38 == 0;
              *(_QWORD *)(v51 + 8) = v49 - 16;
              *(_QWORD *)(v49 + 16) = v38;
              if ( v25 )
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v38 + 8) + 48LL))(a1: v38);
              v38 = v49;
            }
            goto LABEL_55;
          }
LABEL_41:
          v38 = *(_QWORD *)qword_1435FA6C0;
          if ( *(_QWORD *)qword_1435FA6C0 != 0 )
          {
            *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v38;
            *(_QWORD *)v38 = 1;
            --*(_DWORD *)qword_1435FA6D0;
          }
          else
          {
            v69 = v40;
            v67 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
            v40 = v69;
            v38 = v67;
          }
          *(_QWORD *)(v38 + 16) = 0;
          *(_QWORD *)(v38 + 24) = v8;
          ++*(_QWORD *)v8;
          v42 = *(_QWORD *)(qword_143A35A28 + 504);
          *(_DWORD *)(v38 + 36) = v40;
          v43 = *(_QWORD *)(v42 + 16);
          *(_DWORD *)(v38 + 32) = -1;
          v44 = *(_QWORD *)(v43 + 744);
          v45 = *(_QWORD *)(v44 + 8);
          *(_QWORD *)&v46 = v44;
          v47 = v45 | *(_QWORD *)(v38 - 8) & 3LL;
          *(_QWORD *)v45 = v38 - 16;
          *((_QWORD *)&v46 + 1) = v47;
          *(_OWORD *)(v38 - 16) = v46;
          *(_QWORD *)(v44 + 8) = v38 - 16;
LABEL_55:
          ((void (__fastcall *)(__int64, void *, _QWORD *, _QWORD *))unk_142F544C0)(
            a1: v8,
            a2: &unk_14359FC67,
            a3: v9,
            a4: v10);
          if ( qword_143944168 == v8 )
          {
            v25 = (*(_QWORD *)v8)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v8 + 8) + 48LL))(a1: v8);
            qword_143944168 = 0;
          }
          v55 = a1[7];
          v56 = *(_QWORD *)(v55 + 8);
          v57 = *(_QWORD *)(v56 + 40);
          v58 = *(_QWORD **)(v57 + 16);
          *(_QWORD *)(v55 + 8) = *(_QWORD *)(v56 + 48);
          *(_DWORD *)(v57 + 64) = -1;
          if ( v58 != nullptr )
          {
            *(_QWORD *)(v57 + 16) = 0;
            v25 = (*v58)-- == 1;
            if ( v25 )
              (*(void (**)(void))(v58[1] + 48LL))();
          }
          v25 = (*(_QWORD *)v57)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(__int64))(*(_QWORD *)(v57 + 8) + 48LL))(a1: v57);
          *(_QWORD *)(v57 + 120) = 0;
          v25 = (*v9)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v9[1] + 48LL))(a1: v9);
          v25 = (*v10)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v10[1] + 48LL))(a1: v10);
          MEMORY[0x13B00DF80](a1, a2: v39, a3: v41, a4: v38);
          return 0;
        }
      }
      v39 = a1[12];
      v41 = a1[13];
      v40 = 16;
      v38 = a1[14];
      *((_OWORD *)a1 + 6) = 0;
      a1[14] = 0;
      goto LABEL_48;
    }
  }
  v38 = a1[14];
  a1[14] = 0;
  v40 = 13;
  v39 = a1[12];
  v41 = a1[13];
  *((_OWORD *)a1 + 6) = 0;
  goto LABEL_48;
}