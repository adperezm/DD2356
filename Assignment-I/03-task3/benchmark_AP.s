	.file	"benchmark_AP.c"
# GNU C17 (Ubuntu 9.3.0-17ubuntu1~20.04) version 9.3.0 (x86_64-linux-gnu)
#	compiled by GNU C version 9.3.0, GMP version 6.2.0, MPFR version 4.0.2, MPC version 1.1.0, isl version isl-0.22.1-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed:  -imultiarch x86_64-linux-gnu benchmark_AP.c
# -mtune=generic -march=x86-64 -O2 -fverbose-asm
# -fasynchronous-unwind-tables -fstack-protector-strong -Wformat
# -Wformat-security -fstack-clash-protection -fcf-protection
# options enabled:  -fPIC -fPIE -faggressive-loop-optimizations
# -falign-functions -falign-jumps -falign-labels -falign-loops
# -fassume-phsa -fasynchronous-unwind-tables -fauto-inc-dec
# -fbranch-count-reg -fcaller-saves -fcode-hoisting
# -fcombine-stack-adjustments -fcommon -fcompare-elim -fcprop-registers
# -fcrossjumping -fcse-follow-jumps -fdefer-pop
# -fdelete-null-pointer-checks -fdevirtualize -fdevirtualize-speculatively
# -fdwarf2-cfi-asm -fearly-inlining -feliminate-unused-debug-types
# -fexpensive-optimizations -fforward-propagate -ffp-int-builtin-inexact
# -ffunction-cse -fgcse -fgcse-lm -fgnu-runtime -fgnu-unique
# -fguess-branch-probability -fhoist-adjacent-loads -fident -fif-conversion
# -fif-conversion2 -findirect-inlining -finline -finline-atomics
# -finline-functions-called-once -finline-small-functions -fipa-bit-cp
# -fipa-cp -fipa-icf -fipa-icf-functions -fipa-icf-variables -fipa-profile
# -fipa-pure-const -fipa-ra -fipa-reference -fipa-reference-addressable
# -fipa-sra -fipa-stack-alignment -fipa-vrp -fira-hoist-pressure
# -fira-share-save-slots -fira-share-spill-slots
# -fisolate-erroneous-paths-dereference -fivopts -fkeep-static-consts
# -fleading-underscore -flifetime-dse -flra-remat -flto-odr-type-merging
# -fmath-errno -fmerge-constants -fmerge-debug-strings
# -fmove-loop-invariants -fomit-frame-pointer -foptimize-sibling-calls
# -foptimize-strlen -fpartial-inlining -fpeephole -fpeephole2 -fplt
# -fprefetch-loop-arrays -free -freg-struct-return -freorder-blocks
# -freorder-blocks-and-partition -freorder-functions -frerun-cse-after-loop
# -fsched-critical-path-heuristic -fsched-dep-count-heuristic
# -fsched-group-heuristic -fsched-interblock -fsched-last-insn-heuristic
# -fsched-rank-heuristic -fsched-spec -fsched-spec-insn-heuristic
# -fsched-stalled-insns-dep -fschedule-fusion -fschedule-insns2
# -fsemantic-interposition -fshow-column -fshrink-wrap
# -fshrink-wrap-separate -fsigned-zeros -fsplit-ivs-in-unroller
# -fsplit-wide-types -fssa-backprop -fssa-phiopt -fstack-clash-protection
# -fstack-protector-strong -fstdarg-opt -fstore-merging -fstrict-aliasing
# -fstrict-volatile-bitfields -fsync-libcalls -fthread-jumps
# -ftoplevel-reorder -ftrapping-math -ftree-bit-ccp -ftree-builtin-call-dce
# -ftree-ccp -ftree-ch -ftree-coalesce-vars -ftree-copy-prop -ftree-cselim
# -ftree-dce -ftree-dominator-opts -ftree-dse -ftree-forwprop -ftree-fre
# -ftree-loop-if-convert -ftree-loop-im -ftree-loop-ivcanon
# -ftree-loop-optimize -ftree-parallelize-loops= -ftree-phiprop -ftree-pre
# -ftree-pta -ftree-reassoc -ftree-scev-cprop -ftree-sink -ftree-slsr
# -ftree-sra -ftree-switch-conversion -ftree-tail-merge -ftree-ter
# -ftree-vrp -funit-at-a-time -funwind-tables -fverbose-asm
# -fzero-initialized-in-bss -m128bit-long-double -m64 -m80387
# -malign-stringops -mavx256-split-unaligned-load
# -mavx256-split-unaligned-store -mfancy-math-387 -mfp-ret-in-387 -mfxsr
# -mglibc -mieee-fp -mlong-double-80 -mmmx -mno-sse4 -mpush-args -mred-zone
# -msse -msse2 -mstv -mtls-direct-seg-refs -mvzeroupper

	.text
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC4:
	.string	"Execution time iteration %d: %11.8f s\n"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC6:
	.string	"Average: %11.8f \n"
.LC7:
	.string	"Array value: %11.8f s \n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB23:
	.cfi_startproc
	endbr64	
	pushq	%r15	#
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14	#
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13	#
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12	#
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp	#
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx	#
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	leaq	-1196032(%rsp), %r11	#,
	.cfi_def_cfa 11, 1196088
.LPSRL0:
	subq	$4096, %rsp	#,
	orq	$0, (%rsp)	#,
	cmpq	%r11, %rsp	#,
	jne	.LPSRL0
	.cfi_def_cfa_register 7
	subq	$4040, %rsp	#,
	.cfi_def_cfa_offset 1200128
	movsd	.LC1(%rip), %xmm1	#, tmp143
	movsd	.LC2(%rip), %xmm0	#, tmp144
# benchmark_AP.c:7: int main(){
	movq	%fs:40, %rax	# MEM[(<address-space-1> long unsigned int *)40B], tmp150
	movq	%rax, 1200056(%rsp)	# tmp150, D.2676
	xorl	%eax, %eax	# tmp150
	leaq	48(%rsp), %r15	#, tmp142
	leaq	400048(%rsp), %rbx	#, tmp141
	.p2align 4,,10
	.p2align 3
.L2:
# benchmark_AP.c:14:     a[i] = 47.0;
	movsd	%xmm1, (%r15,%rax)	# tmp143, MEM[symbol: a, index: ivtmp.40_14, offset: 0B]
# benchmark_AP.c:15:     b[i] = 3.1415;
	movsd	%xmm0, (%rbx,%rax)	# tmp144, MEM[symbol: b, index: ivtmp.40_14, offset: 0B]
	addq	$8, %rax	#, ivtmp.40
# benchmark_AP.c:13:   for (i = 0; i < N; i++){
	cmpq	$400000, %rax	#, ivtmp.40
	jne	.L2	#,
	xorl	%eax, %eax	# ivtmp.31
	leaq	800048(%rsp), %r14	#, tmp148
	.p2align 4,,10
	.p2align 3
.L3:
# benchmark_AP.c:20:     c[i] = a[i]*b[i];
	movsd	(%r15,%rax), %xmm0	# MEM[symbol: a, index: ivtmp.31_58, offset: 0B], MEM[symbol: a, index: ivtmp.31_58, offset: 0B]
	mulsd	(%rbx,%rax), %xmm0	# MEM[symbol: b, index: ivtmp.31_58, offset: 0B], tmp117
# benchmark_AP.c:20:     c[i] = a[i]*b[i];
	movsd	%xmm0, (%r14,%rax)	# tmp117, MEM[symbol: c, index: ivtmp.31_58, offset: 0B]
	addq	$8, %rax	#, ivtmp.31
# benchmark_AP.c:19:   for(i = 0; i < N; i++)
	cmpq	$400000, %rax	#, ivtmp.31
	jne	.L3	#,
# benchmark_AP.c:25:   totaltime=0;
	pxor	%xmm4, %xmm4	# totaltime
	leaq	24(%rsp), %r13	#, tmp146
	leaq	32(%rsp), %r12	#, tmp147
# benchmark_AP.c:28:   for (j=0;j<repeat;j++)
	xorl	%ebp, %ebp	# j
# benchmark_AP.c:25:   totaltime=0;
	movsd	%xmm4, (%rsp)	# totaltime, %sfp
.L5:
# benchmark_AP.c:53:   i = gettimeofday(&tp,&tzp);
	movq	%r13, %rsi	# tmp146,
	movq	%r12, %rdi	# tmp147,
	call	gettimeofday@PLT	#
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm0, %xmm0	# tmp121
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm1, %xmm1	# tmp124
	xorl	%eax, %eax	# ivtmp.14
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	40(%rsp), %xmm0	# tp.tv_usec, tmp121
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	mulsd	.LC3(%rip), %xmm0	#, tmp122
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	32(%rsp), %xmm1	# tp.tv_sec, tmp124
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	addsd	%xmm1, %xmm0	# tmp124, tmp122
	movsd	%xmm0, 8(%rsp)	# tmp122, %sfp
	.p2align 4,,10
	.p2align 3
.L4:
# benchmark_AP.c:33:             c[i] = a[i]*b[i];
	movsd	(%r15,%rax), %xmm0	# MEM[symbol: a, index: ivtmp.14_12, offset: 0B], MEM[symbol: a, index: ivtmp.14_12, offset: 0B]
	mulsd	(%rbx,%rax), %xmm0	# MEM[symbol: b, index: ivtmp.14_12, offset: 0B], tmp128
# benchmark_AP.c:33:             c[i] = a[i]*b[i];
	movsd	%xmm0, (%r14,%rax)	# tmp128, MEM[symbol: c, index: ivtmp.14_12, offset: 0B]
	addq	$8, %rax	#, ivtmp.14
# benchmark_AP.c:32:           for(i = 0; i < N; i++)
	cmpq	$400000, %rax	#, ivtmp.14
	jne	.L4	#,
# benchmark_AP.c:53:   i = gettimeofday(&tp,&tzp);
	movq	%r13, %rsi	# tmp146,
	movq	%r12, %rdi	# tmp147,
# benchmark_AP.c:35:   	  printf("Execution time iteration %d: %11.8f s\n", j+1, (t2 - t1));
	addl	$1, %ebp	#, j
# benchmark_AP.c:53:   i = gettimeofday(&tp,&tzp);
	call	gettimeofday@PLT	#
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm0, %xmm0	# tmp132
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm1, %xmm1	# tmp135
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	movl	%ebp, %edx	# j,
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	40(%rsp), %xmm0	# tp.tv_usec, tmp132
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	movl	$1, %edi	#,
	movl	$1, %eax	#,
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	mulsd	.LC3(%rip), %xmm0	#, tmp133
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	32(%rsp), %xmm1	# tp.tv_sec, tmp135
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	leaq	.LC4(%rip), %rsi	#,
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	addsd	%xmm1, %xmm0	# tmp135, _44
# benchmark_AP.c:35:   	  printf("Execution time iteration %d: %11.8f s\n", j+1, (t2 - t1));
	subsd	8(%rsp), %xmm0	# %sfp, _7
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	movsd	%xmm0, 8(%rsp)	# _7, %sfp
	call	__printf_chk@PLT	#
# benchmark_AP.c:37: 	  totaltime+=(t2-t1);
	movsd	8(%rsp), %xmm0	# %sfp, _7
	addsd	(%rsp), %xmm0	# %sfp, _7
	movsd	%xmm0, (%rsp)	# _7, %sfp
# benchmark_AP.c:28:   for (j=0;j<repeat;j++)
	cmpl	$10, %ebp	#, j
	jne	.L5	#,
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	leaq	.LC6(%rip), %rsi	#,
	movl	$1, %edi	#,
	movl	$1, %eax	#,
# benchmark_AP.c:40:   printf("Average: %11.8f \n", totaltime/(float)repeat);
	divsd	.LC5(%rip), %xmm0	#, totaltime
# /usr/include/x86_64-linux-gnu/bits/stdio2.h:107:   return __printf_chk (__USE_FORTIFY_LEVEL - 1, __fmt, __va_arg_pack ());
	call	__printf_chk@PLT	#
	movl	$1, %edi	#,
	movl	$1, %eax	#,
	movsd	800056(%rsp), %xmm0	# c,
	leaq	.LC7(%rip), %rsi	#,
	call	__printf_chk@PLT	#
# benchmark_AP.c:45: }
	movq	1200056(%rsp), %rax	# D.2676, tmp151
	xorq	%fs:40, %rax	# MEM[(<address-space-1> long unsigned int *)40B], tmp151
	jne	.L13	#,
	addq	$1200072, %rsp	#,
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax	#
	popq	%rbx	#
	.cfi_def_cfa_offset 48
	popq	%rbp	#
	.cfi_def_cfa_offset 40
	popq	%r12	#
	.cfi_def_cfa_offset 32
	popq	%r13	#
	.cfi_def_cfa_offset 24
	popq	%r14	#
	.cfi_def_cfa_offset 16
	popq	%r15	#
	.cfi_def_cfa_offset 8
	ret	
.L13:
	.cfi_restore_state
	call	__stack_chk_fail@PLT	#
	.cfi_endproc
.LFE23:
	.size	main, .-main
	.text
	.p2align 4
	.globl	mysecond
	.type	mysecond, @function
mysecond:
.LFB24:
	.cfi_startproc
	endbr64	
	subq	$56, %rsp	#,
	.cfi_def_cfa_offset 64
# benchmark_AP.c:48: double mysecond(){
	movq	%fs:40, %rax	# MEM[(<address-space-1> long unsigned int *)40B], tmp97
	movq	%rax, 40(%rsp)	# tmp97, D.2684
	xorl	%eax, %eax	# tmp97
# benchmark_AP.c:53:   i = gettimeofday(&tp,&tzp);
	leaq	8(%rsp), %rsi	#, tmp89
	leaq	16(%rsp), %rdi	#, tmp90
	call	gettimeofday@PLT	#
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm0, %xmm0	# tmp91
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	pxor	%xmm1, %xmm1	# tmp94
# benchmark_AP.c:55: }
	movq	40(%rsp), %rax	# D.2684, tmp98
	xorq	%fs:40, %rax	# MEM[(<address-space-1> long unsigned int *)40B], tmp98
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	24(%rsp), %xmm0	# tp.tv_usec, tmp91
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	mulsd	.LC3(%rip), %xmm0	#, tmp92
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	cvtsi2sdq	16(%rsp), %xmm1	# tp.tv_sec, tmp94
# benchmark_AP.c:54:   return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
	addsd	%xmm1, %xmm0	# tmp94, <retval>
# benchmark_AP.c:55: }
	jne	.L17	#,
	addq	$56, %rsp	#,
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret	
.L17:
	.cfi_restore_state
	call	__stack_chk_fail@PLT	#
	.cfi_endproc
.LFE24:
	.size	mysecond, .-mysecond
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC1:
	.long	0
	.long	1078427648
	.align 8
.LC2:
	.long	3229815407
	.long	1074340298
	.align 8
.LC3:
	.long	2696277389
	.long	1051772663
	.align 8
.LC5:
	.long	0
	.long	1076101120
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
