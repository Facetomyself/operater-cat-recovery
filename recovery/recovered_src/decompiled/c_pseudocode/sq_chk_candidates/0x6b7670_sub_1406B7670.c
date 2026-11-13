void __fastcall sub_1406B7670(
        __int64 a1,
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
        __int64 a12,
        __int64 a13,
        __int64 a14,
        __int64 a15,
        __int64 a16,
        __int64 a17,
        _QWORD *a18)
{
  __int64 v18; // rax
  __int64 v19; // rbx
  __int64 v20; // rdi
  __int64 v21; // rsi
  __int64 v22; // r12
  __m128 *v23; // r13
  __int64 v24; // r15
  __int64 v25; // rbp
  __m128 v26; // xmm0
  _QWORD *v27; // rdx
  int v28; // eax
  __int64 v29; // rbp
  __m128 v30; // xmm0
  __int64 *v31; // rax
  __int64 v32; // r8
  __int64 v33; // rcx
  int v34; // edx
  int v35; // edx
  __m128 *v36; // r12
  __m128 v37; // xmm0
  bool v38; // zf
  __int64 v39; // rax
  __int64 v40; // rdx
  __int64 v41; // r12
  __int64 v42; // rax
  __int64 v43; // rdx
  __int64 v44; // rdx
  __int64 v45; // rdi
  __int64 v46; // rdx
  __int64 v47; // r8
  __int64 *v48; // rdi
  int v49; // edx
  __int64 v50; // rax
  __int64 v51; // r8
  __int64 *v52; // rdi
  int v53; // edx
  __int64 v54; // rax
  __int64 v55; // rax
  __int64 v56; // rdx
  __int64 v57; // r12
  _QWORD *v58; // rcx
  _QWORD *v59; // rdi
  _QWORD *v60; // rdx
  __int64 v61; // rax
  _QWORD *v62; // r12
  _QWORD *v63; // r12
  _QWORD *v64; // rdx
  __int64 v65; // rax
  _QWORD *v66; // rdi
  __int64 v67; // rax
  _QWORD *v68; // rdi
  __int64 v69; // rdx
  __int64 v70; // rdx
  unsigned __int64 v71; // r8
  __int128 v72; // xmm0
  __int64 v73; // rax
  __int64 v74; // xmm5_8
  _QWORD *v75; // rax
  __int64 v76; // rax
  _QWORD *v77; // rsi
  __int64 v78; // rax
  __int64 v79; // rdi
  __int64 *v80; // rax
  __int64 v81; // rdx
  _QWORD *v82; // rdi
  _QWORD *v83; // rbp
  __int64 v84; // r8
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // rdx
  __int64 v88; // rbx
  _QWORD *v89; // rcx
  __int64 v90; // r14
  __int64 v91; // r14
  __int64 v92; // rax
  __int64 v93; // rax
  __int64 v94; // rdx
  unsigned __int64 v95; // r8
  __int128 v96; // xmm0
  __int64 v97; // rax
  __int64 v98; // rdx
  _QWORD *v99; // rax
  _QWORD *v100; // r14
  int v101; // edx
  __int64 v102; // r9
  __int64 v103; // rax
  __int64 v104; // rdx
  unsigned __int64 v105; // r8
  __int128 v106; // xmm0
  __int64 v107; // rax
  __int64 v108; // rax
  __int64 v109; // rdx
  __int64 v110; // r12
  _QWORD *v111; // rcx
  __int64 v112; // rax
  __int64 *v113; // rax
  __int64 v114; // r14
  __int64 v115; // rax
  __int64 v116; // rax
  __int64 v117; // rdx
  unsigned __int64 v118; // r8
  __int128 v119; // xmm0
  __int64 v120; // rax
  __int64 v121; // rax
  __int64 v122; // r8
  __int64 v123; // rax
  _QWORD *v124; // rax
  _QWORD *v125; // rax
  _QWORD *v126; // rax
  __int64 *v127; // rax
  int v128; // [rsp+50h] [rbp+50h]
  int v129; // [rsp+50h] [rbp+50h]
  __int64 v130; // [rsp+58h] [rbp+58h]
  _QWORD *v131; // [rsp+60h] [rbp+60h]
  __int64 v132; // [rsp+60h] [rbp+60h]
  _QWORD *v133; // [rsp+60h] [rbp+60h]
  __int64 v134; // [rsp+60h] [rbp+60h]
  __int64 v135; // [rsp+60h] [rbp+60h]
  __int64 v136; // [rsp+70h] [rbp+70h]

  v25 = *(unsigned int *)(a1 + 8 * v18 + 4496);
  v23->m128_u64[0] = 1;
  v26 = _mm_loadh_ps((const double *)(v25 + 40));
  v23[1].m128_u64[0] = 0;
  v23[2] = v26;
  v27 = *(_QWORD **)(v22 + 32);
  v23[1].m128_u64[1] = 1;
  ++*v27;
  if ( (_DWORD)v18 != 0 )
  {
    v28 = v18 - 1;
    *(_DWORD *)(a1 + 5136) = v28;
    v29 = *(_QWORD *)(a1 + 8LL * v28 + 4496);
    *(_QWORD *)v29 = 1;
  }
  else
  {
    v29 = MEMORY[0x13B00DD60](a1: qword_143A352C8);
  }
  v30 = _mm_loadh_ps((const double *)(v22 + 40));
  *(_QWORD *)(v29 + 16) = 0;
  *(_QWORD *)(v29 + 24) = 1;
  *(__m128 *)(v29 + 32) = v30;
  v31 = (__int64 *)MEMORY[0x13B02A410](a1: qword_143940578, a2: qword_143940620);
  if ( v31 == nullptr || (v130 = *v31, *v31 == 0) )
  {
    v113 = (__int64 *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_143940620);
    if ( v113 == nullptr || (v130 = *v113, *v113 == 0) )
    {
      ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(a1: v19, a2: a10, a3: qword_143940620);
      goto LABEL_100;
    }
  }
  ++*(_QWORD *)v29;
  qword_143A35310(a1: v29, a2: qword_143940648, a3: qword_143940640);
  qword_143A35310(a1: v29, a2: qword_143940650, a3: qword_1439405C8);
  v32 = *(_QWORD *)(v21 + 8);
  v33 = *(_QWORD *)(v19 + 16);
  v34 = *(_DWORD *)(v33 + 5136);
  ++**(_QWORD **)(v32 + 32);
  if ( v34 != 0 )
  {
    v35 = v34 - 1;
    *(_DWORD *)(v33 + 5136) = v35;
    v36 = *(__m128 **)(v33 + 8LL * v35 + 4496);
    v36->m128_u64[0] = 1;
  }
  else
  {
    v134 = v32;
    v112 = MEMORY[0x13B00DD60](a1: qword_143A352C8);
    v32 = v134;
    v36 = (__m128 *)v112;
  }
  v37 = _mm_loadh_ps((const double *)(v32 + 40));
  v36[1].m128_u64[0] = 0;
  v36[2] = v37;
  v36[1].m128_u64[1] = 1;
  qword_143A35310(a1: v29, a2: qword_143940658, a3: v36);
  v38 = v36->m128_u64[0]-- == 1;
  if ( v38 )
    (*(void (__fastcall **)(__m128 *))(v36->m128_u64[1] + 48))(a1: v36);
  qword_143A35310(a1: v29, a2: qword_143940580, a3: qword_143A35200);
  v39 = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_1430EE010)(
          a1: v19,
          a2: qword_143944258,
          a3: qword_1439442C0);
  v40 = *(_QWORD *)(v19 + 56);
  v41 = v39;
  v42 = *(_QWORD *)(v40 + 8);
  *(_QWORD *)(v41 + 120) = v42;
  *(_QWORD *)(v40 + 8) = v41 + 72;
  if ( v42 != 0
    && (*(_BYTE *)(v42 + 69) == 1
     || *(_QWORD *)(v42 + 56) >= (unsigned __int64)(*(_QWORD *)(v42 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v42 + 32) + 168LL)
                                                  + 184)) )
  {
    v98 = *(_QWORD *)(v41 + 112);
    if ( v98 != 0 )
    {
      v99 = *(_QWORD **)(v42 + 40);
      *(_QWORD *)(v98 + 16) = v99;
      if ( v99 != nullptr )
        ++*v99;
    }
  }
  ++*(_QWORD *)v41;
  *(_DWORD *)(v41 + 64) = 0;
  v43 = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_142F58DB0)(a1: v19, a2: v29, a3: qword_143940658);
  if ( v43 != 0 )
  {
    if ( (unsigned __int8)MEMORY[0x13B0CA490](a1: v19, a2: v43, a3: qword_143940580, a4: qword_143A351F8) != 0 )
    {
      qword_143A35310(a1: v29, a2: qword_143940588, a3: qword_143940598);
      v44 = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_142F58DB0)(a1: v19, a2: v29, a3: qword_143940658);
      if ( v44 != 0 )
      {
        if ( (unsigned __int8)MEMORY[0x13B0CA490](a1: v19, a2: v44, a3: qword_143940588, a4: qword_143A35788) != 0 )
        {
          qword_143A35310(a1: v29, a2: qword_143940590, a3: v20);
          v45 = ((__int64 (*)(void))unk_14321AEC0)();
          if ( v45 != 0 )
          {
            v46 = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_142F58DB0)(
                    a1: v19,
                    a2: v29,
                    a3: qword_143940658);
            if ( v46 != 0 )
            {
              if ( (unsigned __int8)MEMORY[0x13B0CA490](a1: v19, a2: v46, a3: qword_143940590, a4: v45) != 0 )
              {
                v131 = (_QWORD *)qword_143A35320(a1: 3);
                qword_143A35310(a1: v131, a2: qword_143940580, a3: qword_143A351F8);
                qword_143A35310(a1: v131, a2: qword_143940588, a3: qword_143A35788);
                v47 = ((__int64 (*)(void))unk_14321AEC0)();
                if ( v47 != 0 )
                {
                  qword_143A35310(a1: v131, a2: qword_143940590, a3: v47);
                  ++*(_QWORD *)qword_143940660;
                  v48 = (__int64 *)((__int64 (__fastcall *)(void *, __int64, __int64, __int64))unk_1430EE8A0)(
                                     a1: &unk_1405FD8B0,
                                     a2: qword_143940668,
                                     a3: qword_143940670,
                                     a4: qword_1439442B8);
                  v49 = qword_143A35310(a1: v29, a2: qword_143940668, a3: v48);
                  v50 = *v48 - 1;
                  if ( v49 != 0 )
                  {
                    *v48 = v50;
                    if ( v50 == 0 )
                      (*(void (__fastcall **)(__int64 *))(v48[1] + 48))(a1: v48);
                    v101 = 18;
                    v100 = *(_QWORD **)(v19 + 112);
                    *(_OWORD *)(v19 + 96) = 0;
                    *(_QWORD *)(v19 + 112) = 0;
                  }
                  else
                  {
                    *v48 = v50;
                    if ( v50 == 0 )
                      (*(void (__fastcall **)(__int64 *))(v48[1] + 48))(a1: v48);
                    v136 = ((__int64 (*)(void))unk_14321AEC0)();
                    if ( v136 != 0 )
                    {
                      v132 = qword_143A35320(a1: 2);
                      qword_143A35310(a1: v132, a2: qword_143940590, a3: v136);
                      qword_143A35310(a1: v132, a2: qword_143940678, a3: qword_1439405C8);
                      ++*(_QWORD *)qword_143940660;
                      v51 = ((__int64 (__fastcall *)(void *, __int64, __int64, __int64))unk_1430EE8A0)(
                              a1: &unk_1405FDDB0,
                              a2: qword_143940680,
                              a3: qword_143940688,
                              a4: qword_1439442A8);
                      if ( *(_QWORD *)qword_1435D24D0 == 0 )
                      {
                        v135 = v51;
                        v124 = (_QWORD *)qword_143A352E0(a1: *(_QWORD *)qword_1435FA560, a2: &unk_1435A0190);
                        if ( v124 == nullptr )
                          goto LABEL_120;
                        ++*v124;
                        v51 = v135;
                        *(_QWORD *)qword_1435D24D0 = v124;
                      }
                      v133 = (_QWORD *)v51;
                      v52 = (__int64 *)((__int64 (__fastcall *)(__int64))unk_142F6A9F0)(a1: v19);
                      v38 = (*v133)-- == 1;
                      if ( v38 )
                        (*(void (__fastcall **)(_QWORD *))(v133[1] + 48LL))(a1: v133);
                      if ( v52 != nullptr )
                      {
                        v53 = qword_143A35310(a1: v29, a2: qword_143940680, a3: v52);
                        v54 = *v52 - 1;
                        *v52 = v54;
                        if ( v53 == 0 )
                        {
                          if ( v54 == 0 )
                            (*(void (__fastcall **)(__int64 *))(v52[1] + 48))(a1: v52);
                          v55 = *(_QWORD *)(v19 + 56);
                          v56 = *(_QWORD *)(v55 + 8);
                          v57 = *(_QWORD *)(v56 + 40);
                          v58 = *(_QWORD **)(v57 + 16);
                          *(_QWORD *)(v55 + 8) = *(_QWORD *)(v56 + 48);
                          *(_DWORD *)(v57 + 64) = -1;
                          if ( v58 != nullptr )
                          {
                            *(_QWORD *)(v57 + 16) = 0;
                            v38 = (*v58)-- == 1;
                            if ( v38 )
                              (*(void (**)(void))(v58[1] + 48LL))();
                          }
                          v38 = (*(_QWORD *)v57)-- == 1;
                          if ( v38 )
                            (*(void (__fastcall **)(__int64))(*(_QWORD *)(v57 + 8) + 48LL))(a1: v57);
                          *(_QWORD *)(v57 + 120) = 0;
                          ((void (__fastcall *)(__int64, __int64))unk_142F90710)(a1: v19, a2: qword_143940690);
                          v59 = (_QWORD *)((__int64 (__fastcall *)(void *, __int64, __int64, __int64))unk_1430EE620)(
                                            a1: &unk_1405FE1D0,
                                            a2: qword_1439405D0,
                                            a3: qword_143940698,
                                            a4: qword_143944298);
                          v60 = *(_QWORD **)qword_1435D24D0;
                          if ( *(_QWORD *)qword_1435D24D0 == 0 )
                          {
                            v125 = (_QWORD *)qword_143A352E0(a1: *(_QWORD *)qword_1435FA560, a2: &unk_1435A0190);
                            v60 = v125;
                            if ( v125 == nullptr )
                              goto LABEL_120;
                            ++*v125;
                            *(_QWORD *)qword_1435D24D0 = v125;
                          }
                          v61 = ((__int64 (__fastcall *)(__int64, _QWORD *, _QWORD *))unk_142F6A9F0)(
                                  a1: v19,
                                  a2: v60,
                                  a3: v59);
                          v38 = (*v59)-- == 1;
                          v62 = (_QWORD *)v61;
                          if ( v38 )
                            (*(void (__fastcall **)(_QWORD *))(v59[1] + 48LL))(a1: v59);
                          qword_143A35310(a1: v29, a2: qword_1439405D0, a3: v62);
                          v38 = (*v62)-- == 1;
                          if ( v38 )
                            (*(void (__fastcall **)(_QWORD *))(v62[1] + 48LL))(a1: v62);
                          ((void (__fastcall *)(__int64, __int64))unk_142F90710)(a1: v19, a2: qword_143940690);
                          v63 = (_QWORD *)((__int64 (__fastcall *)(void *, __int64, __int64, __int64))unk_1430EE620)(
                                            a1: &unk_1405FE5F0,
                                            a2: qword_1439405E0,
                                            a3: qword_1439406A0,
                                            a4: qword_143944288);
                          v64 = *(_QWORD **)qword_1435D24D0;
                          if ( *(_QWORD *)qword_1435D24D0 != 0 )
                            goto LABEL_42;
                          v126 = (_QWORD *)qword_143A352E0(a1: *(_QWORD *)qword_1435FA560, a2: &unk_1435A0190);
                          v64 = v126;
                          if ( v126 != nullptr )
                          {
                            ++*v126;
                            *(_QWORD *)qword_1435D24D0 = v126;
LABEL_42:
                            v65 = ((__int64 (__fastcall *)(__int64, _QWORD *, _QWORD *))unk_142F6A9F0)(
                                    a1: v19,
                                    a2: v64,
                                    a3: v63);
                            v38 = (*v63)-- == 1;
                            v66 = (_QWORD *)v65;
                            if ( v38 )
                              (*(void (__fastcall **)(_QWORD *))(v63[1] + 48LL))(a1: v63);
                            qword_143A35310(a1: v29, a2: qword_1439405E0, a3: v66);
                            v38 = (*v66)-- == 1;
                            if ( v38 )
                              (*(void (__fastcall **)(_QWORD *))(v66[1] + 48LL))(a1: v66);
                            v67 = *(_QWORD *)(v19 + 16);
                            v68 = *(_QWORD **)(v67 + 3624);
                            if ( v68 != nullptr )
                            {
                              v69 = v68[3];
                              --*(_DWORD *)(v67 + 3776);
                              *(_QWORD *)(v67 + 3624) = v69;
                              *v68 = 1;
                            }
                            else
                            {
                              v68 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_142F54770)(
                                                a1: qword_143A35748,
                                                a2: 3);
                            }
                            v70 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
                            v71 = *(_QWORD *)(v70 + 8);
                            *(_QWORD *)&v72 = v70;
                            v73 = v71 | *(v68 - 1) & 3LL;
                            *(_QWORD *)v71 = v68 - 2;
                            v74 = v73;
                            v75 = *(_QWORD **)v21;
                            *((_QWORD *)&v72 + 1) = v74;
                            *((_OWORD *)v68 - 1) = v72;
                            *(_QWORD *)(v70 + 8) = v68 - 2;
                            ++*(_QWORD *)qword_1439405C8;
                            v68[3] = qword_1439405C8;
                            ++*v75;
                            v68[4] = v75;
                            ++*(_QWORD *)v29;
                            v68[5] = v29;
                            *(_DWORD *)(v24 + 40) = 12;
                            v76 = MEMORY[0x13B003A90](a1: v19, a2: qword_143A35768, a3: v68, a4: v23);
                            v38 = (*v68)-- == 1;
                            v77 = (_QWORD *)v76;
                            if ( v38 )
                              (*(void (__fastcall **)(_QWORD *))(v68[1] + 48LL))(a1: v68);
                            if ( v77 != nullptr )
                            {
                              ++*v77;
                              v38 = (*(_QWORD *)v29)-- == 1;
                              if ( v38 )
                                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
                              v38 = (*v77)-- == 1;
                              if ( v38 )
                                (*(void (__fastcall **)(_QWORD *))(v77[1] + 48LL))(a1: v77);
                              *(_DWORD *)(v24 + 40) = 11;
                              v78 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD *))unk_142F6A9F0)(
                                      a1: v19,
                                      a2: v130,
                                      a3: v77);
                              v38 = (*v77)-- == 1;
                              v79 = v78;
                              if ( v38 )
                                (*(void (__fastcall **)(_QWORD *))(v77[1] + 48LL))(a1: v77);
                              if ( v79 != 0 )
                              {
                                MEMORY[0x13B02FE00](a1: qword_143940578, a2: qword_1439405C8, a3: v79);
                                v38 = v23->m128_u64[0]-- == 1;
                                if ( v38 )
                                  (*(void (__fastcall **)(__m128 *))(v23->m128_u64[1] + 48))(a1: v23);
                                v38 = (*(_QWORD *)v29)-- == 1;
                                if ( v38 )
                                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
                                v80 = (__int64 *)MEMORY[0x13B02A410](a1: qword_143940578, a2: qword_143940638);
                                if ( v80 != nullptr && (v81 = *v80, *v80 != 0)
                                  || (v127 = (__int64 *)MEMORY[0x13B02A410](
                                                          a1: *(_QWORD *)qword_1435FA560,
                                                          a2: qword_143940638)) != nullptr
                                  && (v81 = *v127, *v127 != 0) )
                                {
                                  v82 = (_QWORD *)MEMORY[0x13B054620](a1: v19, a2: v81, a3: qword_143A352C8);
                                  if ( v82 != nullptr )
                                  {
                                    v83 = (_QWORD *)qword_143A35320(a1: 4);
                                    qword_143A35310(a1: v83, a2: qword_1439406A8, a3: v82);
                                    v38 = (*v82)-- == 1;
                                    if ( v38 )
                                      (*(void (__fastcall **)(_QWORD *))(v82[1] + 48LL))(a1: v82);
                                    qword_143A35310(a1: v83, a2: qword_1439406B0, a3: qword_143A35788);
                                    qword_143A35310(a1: v83, a2: qword_1439406B8, a3: qword_143A35788);
                                    v84 = ((__int64 (*)(void))unk_14321AD90)();
                                    if ( v84 != 0 )
                                    {
                                      qword_143A35310(a1: v83, a2: qword_143940678, a3: v84);
                                      v85 = ((__int64 (__fastcall *)(void *, __int64, __int64, _QWORD))unk_1430EE3A0)(
                                              a1: &unk_140637240,
                                              a2: qword_1439406C0,
                                              a3: qword_143944278,
                                              a4: 0);
                                      MEMORY[0x13B02FE00](a1: qword_143940578, a2: qword_1439406C0, a3: v85);
                                      v86 = *(_QWORD *)(v19 + 56);
                                      v87 = *(_QWORD *)(v86 + 8);
                                      v88 = *(_QWORD *)(v87 + 40);
                                      v89 = *(_QWORD **)(v88 + 16);
                                      *(_QWORD *)(v86 + 8) = *(_QWORD *)(v87 + 48);
                                      *(_DWORD *)(v88 + 64) = -1;
                                      if ( v89 != nullptr )
                                      {
                                        *(_QWORD *)(v88 + 16) = 0;
                                        v38 = (*v89)-- == 1;
                                        if ( v38 )
                                          (*(void (**)(void))(v89[1] + 48LL))();
                                      }
                                      v38 = (*(_QWORD *)v88)-- == 1;
                                      if ( v38 )
                                        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
                                      *(_QWORD *)(v88 + 120) = 0;
                                      ++*(_QWORD *)qword_1439442C0;
                                      JUMPOUT(0x1406B750ALL);
                                    }
                                    ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(
                                      a1: v19,
                                      a2: a10,
                                      a3: qword_1439405C8);
                                    v38 = (*v83)-- == 1;
                                    if ( v38 )
                                      MEMORY[0x13B0039F0](a1: v83);
                                  }
                                  else
                                  {
                                    *(_OWORD *)(v19 + 96) = 0;
                                    *(_QWORD *)(v19 + 112) = 0;
                                  }
                                }
                                else
                                {
                                  ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(
                                    a1: v19,
                                    a2: a10,
                                    a3: qword_143940638);
                                }
LABEL_156:
                                JUMPOUT(0x1406B7402LL);
                              }
                              *(_OWORD *)(v19 + 96) = 0;
                              *(_QWORD *)(v19 + 112) = 0;
LABEL_100:
                              v38 = v23->m128_u64[0]-- == 1;
                              if ( v38 )
                                (*(void (__fastcall **)(__m128 *))(v23->m128_u64[1] + 48))(a1: v23);
                              v38 = (*(_QWORD *)v29)-- == 1;
                              if ( v38 )
                                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
                              goto LABEL_156;
                            }
                            *(_OWORD *)(v19 + 96) = 0;
                            *(_QWORD *)(v19 + 112) = 0;
LABEL_98:
                            v38 = (*(_QWORD *)v29)-- == 1;
                            if ( v38 )
                              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v29 + 8) + 48LL))(a1: v29);
                            goto LABEL_100;
                          }
LABEL_120:
                          qword_143A35A60(a1: 0);
                          qword_143A35A30(a1: 1);
                          if ( ((__int64 (__fastcall *)(__int64, __m128 *, _QWORD))unk_1430ECB60)(
                                 a1: v19,
                                 a2: v23,
                                 a3: qword_143A35310) == 0 )
                          {
                            v90 = *(_QWORD *)(v19 + 112);
                            *(_OWORD *)(v19 + 96) = 0;
                            *(_QWORD *)(v19 + 112) = 0;
                            v38 = v23->m128_u64[0]-- == 1;
                            if ( v38 )
                              (*(void (__fastcall **)(__m128 *))(v23->m128_u64[1] + 48))(a1: v23);
                            if ( v90 == 0 )
                            {
                              v91 = *(_QWORD *)qword_1435FA6C0;
                              if ( *(_QWORD *)qword_1435FA6C0 != 0 )
                              {
                                *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v91;
                                *(_QWORD *)v91 = 1;
                                --*(_DWORD *)qword_1435FA6D0;
                              }
                              else
                              {
                                v91 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                              }
                              *(_QWORD *)(v91 + 16) = 0;
                              *(_QWORD *)(v91 + 24) = v24;
                              ++*(_QWORD *)v24;
                              v92 = *(_QWORD *)(qword_143A35A28 + 504);
                              *(_DWORD *)(v91 + 32) = -1;
                              v93 = *(_QWORD *)(v92 + 16);
                              *(_DWORD *)(v91 + 36) = 8;
                              v94 = *(_QWORD *)(v93 + 744);
                              v95 = *(_QWORD *)(v94 + 8);
                              *(_QWORD *)&v96 = v94;
                              v97 = v95 | *(_QWORD *)(v91 - 8) & 3LL;
                              *(_QWORD *)v95 = v91 - 16;
                              *((_QWORD *)&v96 + 1) = v97;
                              *(_OWORD *)(v91 - 16) = v96;
                              *(_QWORD *)(v94 + 8) = v91 - 16;
                              JUMPOUT(0x1406B74AFLL);
                            }
                            JUMPOUT(0x1406B740BLL);
                          }
                          JUMPOUT(0x1406B75D1LL);
                        }
                        if ( v54 == 0 )
                          (*(void (__fastcall **)(__int64 *))(v52[1] + 48))(a1: v52);
                        v101 = 25;
                        v100 = *(_QWORD **)(v19 + 112);
                        *(_OWORD *)(v19 + 96) = 0;
                        *(_QWORD *)(v19 + 112) = 0;
                      }
                      else
                      {
                        v101 = 24;
                        v100 = *(_QWORD **)(v19 + 112);
                        *(_OWORD *)(v19 + 96) = 0;
                        *(_QWORD *)(v19 + 112) = 0;
                      }
                    }
                    else
                    {
                      ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(
                        a1: v19,
                        a2: a10,
                        a3: qword_143940630);
                      v101 = 25;
                      v100 = a18;
                    }
                  }
                }
                else
                {
                  ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(a1: v19, a2: a10, a3: qword_143940630);
                  v100 = a18;
                  v38 = (*v131)-- == 1;
                  if ( v38 )
                    (*(void (**)(void))(v131[1] + 48LL))();
                  v101 = 18;
                }
LABEL_86:
                if ( v100 != nullptr )
                {
                  if ( v100[3] != v41 )
                  {
                    v102 = *(_QWORD *)qword_1435FA6C0;
                    if ( *(_QWORD *)qword_1435FA6C0 != 0 )
                    {
                      *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v102;
                      *(_QWORD *)v102 = 1;
                      --*(_DWORD *)qword_1435FA6D0;
                    }
                    else
                    {
                      v128 = v101;
                      v121 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                      v101 = v128;
                      v102 = v121;
                    }
                    *(_QWORD *)(v102 + 24) = v41;
                    ++*(_QWORD *)v41;
                    v103 = *(_QWORD *)(qword_143A35A28 + 504);
                    *(_DWORD *)(v102 + 36) = v101;
                    *(_DWORD *)(v102 + 32) = -1;
                    v104 = *(_QWORD *)(*(_QWORD *)(v103 + 16) + 744LL);
                    v105 = *(_QWORD *)(v104 + 8);
                    *(_QWORD *)&v106 = v104;
                    v107 = v105 | *(_QWORD *)(v102 - 8) & 3LL;
                    *(_QWORD *)v105 = v102 - 16;
                    *((_QWORD *)&v106 + 1) = v107;
                    *(_OWORD *)(v102 - 16) = v106;
                    v38 = *v100 == 0;
                    *(_QWORD *)(v104 + 8) = v102 - 16;
                    *(_QWORD *)(v102 + 16) = v100;
                    if ( v38 )
                      (*(void (__fastcall **)(_QWORD *))(v100[1] + 48LL))(a1: v100);
                  }
                }
                else
                {
                  v114 = *(_QWORD *)qword_1435FA6C0;
                  if ( *(_QWORD *)qword_1435FA6C0 != 0 )
                  {
                    *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v114;
                    *(_QWORD *)v114 = 1;
                    --*(_DWORD *)qword_1435FA6D0;
                  }
                  else
                  {
                    v129 = v101;
                    v123 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                    v101 = v129;
                    v114 = v123;
                  }
                  *(_QWORD *)(v114 + 16) = 0;
                  *(_QWORD *)(v114 + 24) = v41;
                  ++*(_QWORD *)v41;
                  v115 = *(_QWORD *)(qword_143A35A28 + 504);
                  *(_DWORD *)(v114 + 36) = v101;
                  v116 = *(_QWORD *)(v115 + 16);
                  *(_DWORD *)(v114 + 32) = -1;
                  v117 = *(_QWORD *)(v116 + 744);
                  v118 = *(_QWORD *)(v117 + 8);
                  *(_QWORD *)&v119 = v117;
                  v120 = v118 | *(_QWORD *)(v114 - 8) & 3LL;
                  *(_QWORD *)v118 = v114 - 16;
                  *((_QWORD *)&v119 + 1) = v120;
                  *(_OWORD *)(v114 - 16) = v119;
                  *(_QWORD *)(v117 + 8) = v114 - 16;
                }
                ((void (__fastcall *)(__int64, void *, _QWORD))unk_142F544C0)(a1: v41, a2: &unk_14359FC65, a3: 0);
                v108 = *(_QWORD *)(v19 + 56);
                v109 = *(_QWORD *)(v108 + 8);
                v110 = *(_QWORD *)(v109 + 40);
                v111 = *(_QWORD **)(v110 + 16);
                *(_QWORD *)(v108 + 8) = *(_QWORD *)(v109 + 48);
                *(_DWORD *)(v110 + 64) = -1;
                if ( v111 != nullptr )
                {
                  *(_QWORD *)(v110 + 16) = 0;
                  v38 = (*v111)-- == 1;
                  if ( v38 )
                    (*(void (**)(void))(v111[1] + 48LL))();
                }
                v38 = (*(_QWORD *)v110)-- == 1;
                if ( v38 )
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(v110 + 8) + 48LL))(a1: v110);
                *(_QWORD *)(v110 + 120) = 0;
                goto LABEL_98;
              }
LABEL_106:
              v101 = 16;
              v100 = *(_QWORD **)(v19 + 112);
              *(_OWORD *)(v19 + 96) = 0;
              *(_QWORD *)(v19 + 112) = 0;
              goto LABEL_86;
            }
            if ( (unsigned __int8)MEMORY[0x13B018ED0](a1: v19, a2: *(_QWORD *)qword_143A35360) == 0 )
              goto LABEL_106;
            v122 = qword_143940658;
          }
          else
          {
            v122 = qword_143940630;
          }
          ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(a1: v19, a2: a10, a3: v122);
          v101 = 16;
          v100 = a18;
          goto LABEL_86;
        }
      }
      else if ( (unsigned __int8)MEMORY[0x13B018ED0](a1: v19, a2: *(_QWORD *)qword_143A35360) != 0 )
      {
        ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(a1: v19, a2: a10, a3: qword_143940658);
        v101 = 15;
        v100 = a18;
        goto LABEL_86;
      }
      v101 = 15;
      v100 = *(_QWORD **)(v19 + 112);
      *(_OWORD *)(v19 + 96) = 0;
      *(_QWORD *)(v19 + 112) = 0;
      goto LABEL_86;
    }
  }
  else if ( (unsigned __int8)MEMORY[0x13B018ED0](a1: v19, a2: *(_QWORD *)qword_143A35360) != 0 )
  {
    ((void (__fastcall *)(__int64, __int64, __int64))unk_142F6E530)(a1: v19, a2: a10, a3: qword_143940658);
    v101 = 14;
    v100 = a18;
    goto LABEL_86;
  }
  v100 = *(_QWORD **)(v19 + 112);
  *(_QWORD *)(v19 + 112) = 0;
  v101 = 14;
  *(_OWORD *)(v19 + 96) = 0;
  goto LABEL_86;
}