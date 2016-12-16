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
errn 3 m    ��������  ��  ��  ��  ��  ��   #  4 5 4 l     ��������  ��  ��   5  6 7 6 l     �� 8 9��   8 T NCheck that the iTunes Library XML file exists. If it does not, tell use to set    9 � : : � C h e c k   t h a t   t h e   i T u n e s   L i b r a r y   X M L   f i l e   e x i s t s .   I f   i t   d o e s   n o t ,   t e l l   u s e   t o   s e t 7  ; < ; l     �� = >��   = ' !option in the iTunes preferences.    > � ? ? B o p t i o n   i n   t h e   i T u n e s   p r e f e r e n c e s . <  @ A @ l  % , B���� B r   % , C D C l  % * E���� E I  % *�� F��
�� .sysoexecTEXT���     TEXT F m   % & G G � H H ` e c h o   $ H O M E / M u s i c / i T u n e s / i T u n e s   M u s i c   L i b r a r y . x m l��  ��  ��   D o      ���� 0 	ituneslib 	iTunesLib��  ��   A  I J I l  - M K���� K O   - M L M L Z   1 L N O���� N H   1 9 P P l  1 8 Q���� Q I  1 8�� R��
�� .coredoexbool        obj  R c   1 4 S T S o   1 2���� 0 	ituneslib 	iTunesLib T m   2 3��
�� 
psxf��  ��  ��   O k   < H U U  V W V I  < A�� X��
�� .sysodlogaskr        TEXT X m   < = Y Y � Z Zz C o u l d   n o t   f i n d   t h e   i T u n e s   L i b r a r y   X M L   f i l e .   P l e a s e   m a k e   s u r e   t h a t   t h e   ' S h a r e   i T u n e s   L i b r a r y   X M L   w i t h   o t h e r   a p p l i c a t i o n '   o p t i o n s   i s   s e t   u n d e r   i T u n e s   P r e f e r e n c e   >   A d v a n c e d   a n d   t h e n   t r y   a g a i n .��   W  [�� [ R   B H���� \
�� .ascrerr ****      � ****��   \ �� ]��
�� 
errn ] m   D E��������  ��  ��  ��   M m   - . ^ ^�                                                                                  MACS  alis    t  MacintoshSSD               �dH+     7
Finder.app                                                      '�϶tE        ����  	                CoreServices    �e�      ϶��       7   4   3  6MacintoshSSD:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c i n t o s h S S D  &System/Library/CoreServices/Finder.app  / ��  ��  ��   J  _ ` _ l     ��������  ��  ��   `  a b a l     �� c d��   c 0 *Get track IDs for selected files in iTunes    d � e e T G e t   t r a c k   I D s   f o r   s e l e c t e d   f i l e s   i n   i T u n e s b  f g f l  N � h���� h O   N � i j i Z   T � k l�� m k >  T \ n o n 1   T Y��
�� 
sele o J   Y [����   l l  _ � p q r p k   _ � s s  t u t r   _ f v w v m   _ b x x � y y  ' w o      ���� 0 trackids trackIDs u  z�� z X   g � {�� | { r    � } ~ } b    �  �  b    � � � � o    ����� 0 trackids trackIDs � l  � � ����� � n   � � � � � 1   � ���
�� 
pDID � o   � ����� 0 atrack aTrack��  ��   � m   � � � � � � �    ~ o      ���� 0 trackids trackIDs�� 0 atrack aTrack | l  j o ����� � 1   j o��
�� 
sele��  ��  ��   q ! Check if something selected    r � � � 6 C h e c k   i f   s o m e t h i n g   s e l e c t e d��   m k   � � � �  � � � I  � ��� ���
�� .sysodlogaskr        TEXT � m   � � � � � � � * N o   t r a c k s   s e l e c t e d ! ! !��   �  ��� � l  � � � � � � R   � ����� �
�� .ascrerr ****      � ****��   � �� ���
�� 
errn � m   � ���������   �  Quite the program    � � � � " Q u i t e   t h e   p r o g r a m��   j m   N Q � ��                                                                                  hook  alis    N  MacintoshSSD               �dH+     Y
iTunes.app                                                      F�Ϗ{�        ����  	                Applications    �e�      Ϗ��       Y  %MacintoshSSD:Applications: iTunes.app    
 i T u n e s . a p p    M a c i n t o s h S S D  Applications/iTunes.app   / ��  ��  ��   g  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � ! Prompt where to store files    � � � � 6 P r o m p t   w h e r e   t o   s t o r e   f i l e s �  � � � l  � � ����� � r   � � � � � I  � ����� �
�� .sysostflalis    ��� null��   � �� � �
�� 
prmp � m   � � � � � � � * C h o o s e   O u t p u t   F o l d e r . � �� ���
�� 
dflc � l  � � ����� � I  � ��� ���
�� .earsffdralis        afdr � m   � ���
�� afdmdesk��  ��  ��  ��   � o      ���� 0 destdir destDir��  ��   �  � � � l  � � � � � � r   � � � � � l  � � ����� � l  � � ����� � n   � � � � � 1   � ���
�� 
strq � n   � � � � � 1   � ���
�� 
psxp � l  � � ����� � c   � � � � � o   � ����� 0 destdir destDir � m   � ���
�� 
alis��  ��  ��  ��  ��  ��   � o      ���� 0 destdir destDir �  redefine    � � � �  r e d e f i n e �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � e _Set up the beginning part of command with path to command, destination directory, and track IDs    � � � � � S e t   u p   t h e   b e g i n n i n g   p a r t   o f   c o m m a n d   w i t h   p a t h   t o   c o m m a n d ,   d e s t i n a t i o n   d i r e c t o r y ,   a n d   t r a c k   I D s �  � � � l  � � ����� � r   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � o   � ����� 0 profile   � m   � � � � � � �  ;   � o   � ����� 0 
convertdir 
convertDir � m   � � � � � � � 2 i T u n e s _ m u s i c _ c o n v e r t e r . p y � m   � � � � � � �    - d   � o   � ����� 0 destdir destDir � m   � � � � � � �    - t   � o   � ����� 0 trackids trackIDs � m   � � � � � � �  ' � o      ���� 0 cnvtcmd cnvtCmd��  ��   �  � � � l     �������  ��  �   �  � � � l     �~ � ��~   � # Prompt to set the audio codec    � � � � : P r o m p t   t o   s e t   t h e   a u d i o   c o d e c �  � � � l  � ��}�| � I  ��{ � �
�{ .sysodlogaskr        TEXT � m   � � � � � � � $ S e l e c t   a u d i o   c o d e c � �z � �
�z 
btns � J  
 � �  � � � m   � � � � �  F L A C �  ��y � m   � � � � �  M P 3�y   � �x � �
�x 
dflt � m  �w�w  � �v ��u
�v 
disp � m  �t�t �u  �}  �|   �  � � � l $   r  $ n    1   �s
�s 
bhit 1  �r
�r 
rslt o      �q�q 	0 codec   % get audio codec from user input    � > g e t   a u d i o   c o d e c   f r o m   u s e r   i n p u t � 	 l %4

 r  %4 b  %0 b  %, o  %(�p�p 0 cnvtcmd cnvtCmd m  (+ �    - c   o  ,/�o�o 	0 codec   o      �n�n 0 cnvtcmd cnvtCmd + %Append the audio codec to the command    � J A p p e n d   t h e   a u d i o   c o d e c   t o   t h e   c o m m a n d	  l     �m�l�k�m  �l  �k    l     �j�j   6 0If the MP3 codec is to be used, set the bit rate    � ` I f   t h e   M P 3   c o d e c   i s   t o   b e   u s e d ,   s e t   t h e   b i t   r a t e  l 5��i�h Z  5� !�g�f  = 5<"#" o  58�e�e 	0 codec  # m  8;$$ �%%  M P 3! k  ?~&& '(' l ??�d)*�d  )  Prompt to set MP3 quality   * �++ 2 P r o m p t   t o   s e t   M P 3   q u a l i t y( ,-, I ?^�c./
�c .sysodlogaskr        TEXT. m  ?B00 �11 2 P l e s e   s e l e c t   M P 3   q u a l i t y ./ �b23
�b 
btns2 J  EP44 565 m  EH77 �88  1 6 0 k6 9:9 m  HK;; �<<  1 9 2 k: =�a= m  KN>> �??  3 2 0 k�a  3 �`@A
�` 
dflt@ m  ST�_�_ A �^B�]
�^ 
dispB m  WX�\�\ �]  - CDC l _jEFGE r  _jHIH n  _fJKJ 1  bf�[
�[ 
bhitK 1  _b�Z
�Z 
rsltI o      �Y�Y 0 bitrate bitRateF  get bit_rate from file   G �LL , g e t   b i t _ r a t e   f r o m   f i l eD M�XM l k~NOPN r  k~QRQ b  kzSTS b  kvUVU b  krWXW o  kn�W�W 0 cnvtcmd cnvtCmdX m  nqYY �ZZ    - b  V m  ru[[ �\\   T o  vy�V�V 0 bitrate bitRateR o      �U�U 0 cnvtcmd cnvtCmdO , &Append the MP3 bit rate to the command   P �]] L A p p e n d   t h e   M P 3   b i t   r a t e   t o   t h e   c o m m a n d�X  �g  �f  �i  �h   ^_^ l     �T�S�R�T  �S  �R  _ `a` l     �Qbc�Q  b . (Run conversion/copying of selected files   c �dd P R u n   c o n v e r s i o n / c o p y i n g   o f   s e l e c t e d   f i l e sa efe l ��g�P�Og r  ��hih I ���Nj�M
�N .sysoexecTEXT���     TEXTj o  ���L�L 0 cnvtcmd cnvtCmd�M  i 1      �K
�K 
rslt�P  �O  f klk l ��m�J�Im I ���Hno
�H .sysonotfnull��� ��� TEXTn m  ��pp �qq B i T u n e s   m u s i c   c o n v e r s i o n   c o m p l e t e !o �Gr�F
�G 
apprr m  ��ss �tt  c o n v e r t _ m u s i c�F  �J  �I  l u�Eu l ��v�D�Cv I ���Bw�A
�B .sysoexecTEXT���     TEXTw m  ��xx �yy � i f   [   - f   / S y s t e m / L i b r a r y / S o u n d s / G l a s s . a i f f   ] ;   t h e n   a f p l a y   / S y s t e m / L i b r a r y / S o u n d s / G l a s s . a i f f ;   f i�A  �D  �C  �E       �@z{�@  z �?
�? .aevtoappnull  �   � ****{ �>|�=�<}~�;
�> .aevtoappnull  �   � ****| k    �  
��  ��  "��  @��  I��  f��  ���  ���  ���  ���  ��� �� �� e�� k�� u�:�:  �=  �<  } �9�9 0 atrack aTrack~ C �8 �7�6 ) /�5�4�3 G�2 ^�1�0 Y ��/ x�.�-�,�+�* � ��) ��(�'�&�%�$�#�"�!�  � � � � �� �� � �������$07;>�Y[p�s�x�8 0 profile  
�7 .sysoexecTEXT���     TEXT�6 0 
convertdir 
convertDir
�5 .sysodlogaskr        TEXT
�4 
errn�3���2 0 	ituneslib 	iTunesLib
�1 
psxf
�0 .coredoexbool        obj 
�/ 
sele�. 0 trackids trackIDs
�- 
kocl
�, 
cobj
�+ .corecnte****       ****
�* 
pDID
�) 
prmp
�( 
dflc
�' afdmdesk
�& .earsffdralis        afdr�% 
�$ .sysostflalis    ��� null�# 0 destdir destDir
�" 
alis
�! 
psxp
�  
strq� 0 cnvtcmd cnvtCmd
� 
btns
� 
dflt
� 
disp� 
� 
rslt
� 
bhit� 	0 codec  � 0 bitrate bitRate
� 
appr
� .sysonotfnull��� ��� TEXT�;��E�O��%j E�O��  �j O)��lhY hO�j E�O� ��&j  �j O)��lhY hUOa  T*a ,jv ;a E` O -*a ,[a a l kh  _ �a ,%a %E` [OY��Y a j O)��lhUO*a a a a j a   E` !O_ !a "&a #,a $,E` !O�a %%�%a &%a '%_ !%a (%_ %a )%E` *Oa +a ,a -a .lva /la 0ka 1 O_ 2a 3,E` 4O_ *a 5%_ 4%E` *O_ 4a 6  Da 7a ,a 8a 9a :mva /la 0ka 1 O_ 2a 3,E` ;O_ *a <%a =%_ ;%E` *Y hO_ *j E` 2Oa >a ?a @l AOa Bj ascr  ��ޭ