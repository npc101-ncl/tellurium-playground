�}q (X   durationqKX   antStrqX�   
model test_model()
    var A
    var B
    
    R1: ->A; k1
    R2: A->; k2*A*B
    R3: ->B; k3*A
    R4: B->; k4*B
    
    A = 0;
    B = 0;
    
    k1 = 1;
    k2 = 2;
    k3 = 3;
    k4 = 4;

end
qX   PEDataqcpandas.core.frame
DataFrame
q)�q}q(X   _dataqcpandas.core.internals.managers
BlockManager
q	)�q
(]q(cpandas.core.indexes.base
_new_Index
qcpandas.core.indexes.base
Index
q}q(X   dataqcnumpy.core.multiarray
_reconstruct
qcnumpy
ndarray
qK �qCbq�qRq(KK�qcnumpy
dtype
qX   O8qK K�qRq(KX   |qNNNJ����J����K?tqb�]q(X   timeqX   AqX   Bq etq!bX   nameq"Nu�q#Rq$hcpandas.core.indexes.numeric
Int64Index
q%}q&(hhhK �q'h�q(Rq)(KK
�q*hX   i8q+K K�q,Rq-(KX   <q.NNNJ����J����K tq/b�CP        
                     (       2       <       F       P       Z       q0tq1bh"Nu�q2Rq3e]q4hhK �q5h�q6Rq7(KKK
�q8hX   f8q9K K�q:Rq;(Kh.NNNJ����J����K tq<b�C�        2ogH���?2ogH���?e�M6�d�?2ogH���?�@�_)�?e�M6�d�?L�Z�R��?2ogH���?]t�E�?        "z�?���?[�Im��?�p@鏪�?	��B���?��^xf�?0�<�v�?�Ն��!�?�!�<^�?w�q�d�?        ��ݧ�N�?��� 7�?��X�0�?SzG��C�?�����?�#>4�?;6x��[�?��
��?��0�}�?q=tq>ba]q?hh}q@(hhhK �qAh�qBRqC(KK�qDh�]qE(hhh etqFbh"Nu�qGRqHa}qIX   0.14.1qJ}qK(X   axesqLhX   blocksqM]qN}qO(X   valuesqPh7X   mgr_locsqQcbuiltins
slice
qRK KK�qSRqTuaustqUbX   _typqVX	   dataframeqWX	   _metadataqX]qYubX   idxCaseqZX   0-0q[X   runNameq\X   tor0q]u.