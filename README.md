COMPILE:
    To compile run:

    $ cython selfrepairing.pyx (not needed)
    $ python setup.py build
    
    ''Note'': After compiling you might want to move
    'selfrepairing.so'  to the working dir by (or equivalent):

    $ cp build/lib.linux-i686-2.7/selfrepairing.so .

TEST 1:
    The code in test.py is the best point to start reading and
    understanding how selfrepairing.so works. Execute the following:
    
    $ python test.py

TEST 2:
    Files "decode.py" and "encode.py" include a real example of how
    to encode and decode files using SelfRepairing codes.

    Run:
    
    $ python encode.py somefile.dat
    
    to encode any given file 'somefile.dat' to a list of 'n=7' blocks:
      - somefile.dat_0
      - somefile.dat_1
      - somefile.dat_2
      - somefile.dat_3
      - somefile.dat_4
      - somefile.dat_5
      - somefile.dat_6
    
    After the encoding we can check the repair property as follows
    (repairing block 0 from blocks 1 and 2):
   
    $ rm somefile.dat_0
    $ python xor.py somefile.dat_1 somefile.dat_2 somefile.dat_0

    Finally, we can try the decoding property as follows:
    
    $ rm somefile.dat_2 somefile.dat_4 somefile.dat_5 somefile.dat_6
    $ python decode.py somefile.dat
    $ diff somefile.dat somefile.dat_decoded

FILES:
    * Jerasure Library:
        - galois.c
        - galois.h
        - jerasure.c
        - jerasure.h
        - jerasure.pxd
    
    * HSRC code:
        - selfrepairing.pyx

    * Test and examples:
        - test.py
        - encode.py
        - decode.py
        - xor.py
