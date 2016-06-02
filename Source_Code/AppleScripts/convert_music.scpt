FasdUAS 1.101.10   ��   ��    k             l     ��  ��    4 .Set up command to source the bash profile file     � 	 	 \ S e t   u p   c o m m a n d   t o   s o u r c e   t h e   b a s h   p r o f i l e   f i l e   
  
 l     ����  r         m        �   � i f   [   - f   $ H O M E / . p r o f i l e   ] ;   t h e n   s o u r c e   $ H O M E / . p r o f i l e ;   e l i f   [   - f   $ H O M E / . b a s h _ p r o f i l e   ] ;   t h e n   s o u r c e   $ H O M E / . b a s h _ p r o f i l e ;   f i  o      ���� 0 profile  ��  ��        l    ����  r        I   �� ��
�� .sysoexecTEXT���     TEXT  b        o    ���� 0 profile    m       �   * ;   e c h o   $ i T u n e s C o n v e r t��    o      ���� 0 
convertdir 
convertDir��  ��        l     ��������  ��  ��        l     ��   ��    A ;If the iTunesConvert path is NOT returned, stop the program      � ! ! v I f   t h e   i T u n e s C o n v e r t   p a t h   i s   N O T   r e t u r n e d ,   s t o p   t h e   p r o g r a m   " # " l   $ $���� $ Z    $ % &���� % =    ' ( ' o    ���� 0 
convertdir 
convertDir ( m     ) ) � * *   & k      + +  , - , I   �� .��
�� .sysodlogaskr        TEXT . m     / / � 0 0 x I t   a p p e a r s   t h e r e   w a s   a n   e r r o r   d u r i n g   i n s t a l l a t i o n . . . E x i t i n g !��   -  1�� 1 R     ���� 2
�� .ascrerr ****      � ****��   2 �� 3��
�� 
errn 3 m    ��������  ��  ��  ��  ��  ��   #  4 5 4 l     ��������  ��  ��   5  6 7 6 l     �� 8 9��   8 0 *Get track IDs for selected files in iTunes    9 � : : T G e t   t r a c k   I D s   f o r   s e l e c t e d   f i l e s   i n   i T u n e s 7  ; < ; l  % e =���� = O   % e > ? > Z   ) d @ A�� B @ >  ) / C D C 1   ) ,��
�� 
sele D J   , .����   A l  2 Z E F G E k   2 Z H H  I J I r   2 5 K L K m   2 3 M M � N N  ' L o      ���� 0 trackids trackIDs J  O�� O X   6 Z P�� Q P r   H U R S R b   H S T U T b   H O V W V o   H I���� 0 trackids trackIDs W l  I N X���� X n   I N Y Z Y 1   J N��
�� 
pDID Z o   I J���� 0 atrack aTrack��  ��   U m   O R [ [ � \ \    S o      ���� 0 trackids trackIDs�� 0 atrack aTrack Q l  9 < ]���� ] 1   9 <��
�� 
sele��  ��  ��   F ! Check if something selected    G � ^ ^ 6 C h e c k   i f   s o m e t h i n g   s e l e c t e d��   B I  ] d�� _��
�� .sysodlogaskr        TEXT _ m   ] ` ` ` � a a * N o   t r a c k s   s e l e c t e d ! ! !��   ? m   % & b b�                                                                                  hook  alis    N  MacintoshSSD               �dH+     Y
iTunes.app                                                      F�Ϗ{�        ����  	                Applications    �e�      Ϗ��       Y  %MacintoshSSD:Applications: iTunes.app    
 i T u n e s . a p p    M a c i n t o s h S S D  Applications/iTunes.app   / ��  ��  ��   <  c d c l     ��������  ��  ��   d  e f e l     �� g h��   g ! Prompt where to store files    h � i i 6 P r o m p t   w h e r e   t o   s t o r e   f i l e s f  j k j l  f � l���� l r   f � m n m I  f }���� o
�� .sysostflalis    ��� null��   o �� p q
�� 
prmp p m   j m r r � s s * C h o o s e   O u t p u t   F o l d e r . q �� t��
�� 
dflc t l  p w u���� u I  p w�� v��
�� .earsffdralis        afdr v m   p s��
�� afdmdesk��  ��  ��  ��   n o      ���� 0 destdir destDir��  ��   k  w x w l  � � y z { y r   � � | } | l  � � ~���� ~ l  � � ����  n   � � � � � 1   � ���
�� 
strq � n   � � � � � 1   � ���
�� 
psxp � l  � � ����� � c   � � � � � o   � ����� 0 destdir destDir � m   � ���
�� 
alis��  ��  ��  ��  ��  ��   } o      ���� 0 destdir destDir z  redefine    { � � �  r e d e f i n e x  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � e _Set up the beginning part of command with path to command, destination directory, and track IDs    � � � � � S e t   u p   t h e   b e g i n n i n g   p a r t   o f   c o m m a n d   w i t h   p a t h   t o   c o m m a n d ,   d e s t i n a t i o n   d i r e c t o r y ,   a n d   t r a c k   I D s �  � � � l  � � ����� � r   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � o   � ����� 0 profile   � m   � � � � � � �  ;   � o   � ����� 0 
convertdir 
convertDir � m   � � � � � � � 2 i T u n e s _ m u s i c _ c o n v e r t e r . p y � m   � � � � � � �    - d   � o   � ����� 0 destdir destDir � m   � � � � � � �    - t   � o   � ����� 0 trackids trackIDs � m   � � � � � � �  ' � o      ���� 0 cnvtcmd cnvtCmd��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � # Prompt to set the audio codec    � � � � : P r o m p t   t o   s e t   t h e   a u d i o   c o d e c �  � � � l  � � ����� � I  � ��� � �
�� .sysodlogaskr        TEXT � m   � � � � � � � $ S e l e c t   a u d i o   c o d e c � �� � �
�� 
btns � J   � � � �  � � � m   � � � � � � �  F L A C �  ��� � m   � � � � � � �  M P 3��   � �� � �
�� 
dflt � m   � �����  � �� ���
�� 
disp � m   � ����� ��  ��  ��   �  � � � l  � � � � � � r   � � � � � n   � � � � � 1   � ���
�� 
bhit � 1   � ���
�� 
rslt � o      ���� 	0 codec   � % get audio codec from user input    � � � � > g e t   a u d i o   c o d e c   f r o m   u s e r   i n p u t �  � � � l  � � � � � � r   � � � � � b   � � � � � b   � � � � � o   � ����� 0 cnvtcmd cnvtCmd � m   � � � � � � �    - c   � o   � ����� 	0 codec   � o      ���� 0 cnvtcmd cnvtCmd � + %Append the audio codec to the command    � � � � J A p p e n d   t h e   a u d i o   c o d e c   t o   t h e   c o m m a n d �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � 6 0If the MP3 codec is to be used, set the bit rate    � � � � ` I f   t h e   M P 3   c o d e c   i s   t o   b e   u s e d ,   s e t   t h e   b i t   r a t e �  � � � l  �> ����� � Z   �> � ����� � =  � � � � � o   � ����� 	0 codec   � m   � � � � � � �  M P 3 � k   �: � �  � � � l  � ��� � ���   �  Prompt to set MP3 quality    � � � � 2 P r o m p t   t o   s e t   M P 3   q u a l i t y �  � � � I  ��� � �
�� .sysodlogaskr        TEXT � m   � � � � � � � 2 P l e s e   s e l e c t   M P 3   q u a l i t y . � �� � �
�� 
btns � J   � �    m   �  1 6 0 k  m   �  1 9 2 k �� m  
		 �

  3 2 0 k��   � ��
�� 
dflt m  ����  ����
�� 
disp m  ���� ��   �  l & r  & n  " 1  "�
� 
bhit 1  �~
�~ 
rslt o      �}�} 0 bitrate bitRate  get bit_rate from file    � , g e t   b i t _ r a t e   f r o m   f i l e �| l ': r  ': b  '6 b  '2 !  b  '."#" o  '*�{�{ 0 cnvtcmd cnvtCmd# m  *-$$ �%%    - b  ! m  .1&& �''    o  25�z�z 0 bitrate bitRate o      �y�y 0 cnvtcmd cnvtCmd , &Append the MP3 bit rate to the command    �(( L A p p e n d   t h e   M P 3   b i t   r a t e   t o   t h e   c o m m a n d�|  ��  ��  ��  ��   � )*) l     �x�w�v�x  �w  �v  * +,+ l     �u-.�u  - . (Run conversion/copying of selected files   . �// P R u n   c o n v e r s i o n / c o p y i n g   o f   s e l e c t e d   f i l e s, 010 l ?J2�t�s2 r  ?J343 I ?F�r5�q
�r .sysoexecTEXT���     TEXT5 o  ?B�p�p 0 cnvtcmd cnvtCmd�q  4 1      �o
�o 
rslt�t  �s  1 676 l KX8�n�m8 I KX�l9:
�l .sysonotfnull��� ��� TEXT9 m  KN;; �<< B i T u n e s   m u s i c   c o n v e r s i o n   c o m p l e t e !: �k=�j
�k 
appr= m  QT>> �??  c o n v e r t _ m u s i c�j  �n  �m  7 @�i@ l Y`A�h�gA I Y`�fB�e
�f .sysoexecTEXT���     TEXTB m  Y\CC �DD � i f   [   - f   / S y s t e m / L i b r a r y / S o u n d s / G l a s s . a i f f   ] ;   t h e n   a f p l a y   / S y s t e m / L i b r a r y / S o u n d s / G l a s s . a i f f ;   f i�e  �h  �g  �i       �dEF�d  E �c
�c .aevtoappnull  �   � ****F �bG�a�`HI�_
�b .aevtoappnull  �   � ****G k    `JJ  
KK  LL  "MM  ;NN  jOO  wPP  �QQ  �RR  �SS  �TT  �UU 0VV 6WW @�^�^  �a  �`  H �]�] 0 atrack aTrackI = �\ �[�Z ) /�Y�X�W b�V M�U�T�S�R�Q [ `�P r�O�N�M�L�K�J�I�H�G � � � � ��F ��E � ��D�C�B�A�@�? � � �	�>$&;�=>�<C�\ 0 profile  
�[ .sysoexecTEXT���     TEXT�Z 0 
convertdir 
convertDir
�Y .sysodlogaskr        TEXT
�X 
errn�W��
�V 
sele�U 0 trackids trackIDs
�T 
kocl
�S 
cobj
�R .corecnte****       ****
�Q 
pDID
�P 
prmp
�O 
dflc
�N afdmdesk
�M .earsffdralis        afdr�L 
�K .sysostflalis    ��� null�J 0 destdir destDir
�I 
alis
�H 
psxp
�G 
strq�F 0 cnvtcmd cnvtCmd
�E 
btns
�D 
dflt
�C 
disp�B 
�A 
rslt
�@ 
bhit�? 	0 codec  �> 0 bitrate bitRate
�= 
appr
�< .sysonotfnull��� ��� TEXT�_a�E�O��%j E�O��  �j O)��lhY hO� =*�,jv -�E�O #*�,[��l kh  ͠a ,%a %E�[OY��Y 	a j UO*a a a a j a  E` O_ a &a ,a ,E` O�a %�%a  %a !%_ %a "%�%a #%E` $Oa %a &a 'a (lva )la *ka + O_ ,a -,E` .O_ $a /%_ .%E` $O_ .a 0  Da 1a &a 2a 3a 4mva )la *ka + O_ ,a -,E` 5O_ $a 6%a 7%_ 5%E` $Y hO_ $j E` ,Oa 8a 9a :l ;Oa <j  ascr  ��ޭ