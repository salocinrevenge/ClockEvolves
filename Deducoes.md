# Colisão elástica de dois corpos
Há dois corpos com massas $M$ e $m$ e velocidades iniciais $V_i$ e $v_i$, respectivamente.
Após a colisão, os corpos terão suas velocidade finais alteradas para $V_f$ e $v_f$.
A colisao é elástica, portanto, a energia cinética é conservada.
As velocidades são descritas de forma vetorial.

Pela conservação da energia cinética, temos:
    $\frac{MV_i^2}{2} + \frac{mv_i^2}{2} = \frac{MV_f^2}{2} + \frac{mv_f^2}{2}$

Removendo os denominadores:
    $MV_i^2 + mv_i^2 = MV_f^2 + mv_f^2 \implies M(V_i^2 - V_f^2)= m(v_f^2 - v_i^2)$    : (I)

e pela conservação do momento linear, temos:
    $MV_{i} + mv_{i} = MV_{f} + mv_{f}\implies M(V_i - V_f)= m(v_f - v_i)$      : (II)


dividindo (I) por (II):
    $\frac{V_i^2 - V_f^2}{V_i - V_f} = \frac{v_f^2 - v_i^2}{v_f - v_i} \implies \frac{(V_i - V_f)(V_i + V_f)}{V_i - V_f} = \frac{(v_f - v_i)(v_f + v_i)}{v_f - v_i}$

Chagando em: $(V_i+V_f) = (v_f+v_i)$ : (III)

isolando na equação do momento:
    $MV_{i} + mv_{i} = MV_{f} + mv_{f}\implies V_f = V_{i} + \frac{m}{M}(v_{i} - v_f)$

Isolando na equação (III): $V_f = v_i+v_f-V_i$

igualando as duas equações:
    $V_{i} + \frac{m}{M}(v_{i} - v_f) = v_i+v_f-V_i$ $\implies$ $v_f + \frac{m}{M}v_f = 2V_i-v_i + \frac{m}{M}v_i$
    
Isolando $v_f$ temos:  $v_f(1 + \frac{m}{M}) = 2V_i-v_i + \frac{m}{M}v_i$ $\implies$ $v_f = \frac{2V_i-v_i + \frac{m}{M}v_i}{1 + \frac{m}{M}}$ $\implies$ $v_f = \frac{2V_i-v_i + \frac{m}{M}v_i}{\frac{M+m}{M}}$
    
Resultando em: $v_f = \frac{V_iM-v_iM + mv_i}{M+m} = \frac{2M}{M+m}V_i + \frac{m-M}{M+m}v_i$

E para $V_f$ temos: $V_f = v_i+v_f-V_i$ $\implies$ $V_f = v_i + \frac{2M}{M+m}V_i + \frac{m-M}{M+m}v_i - V_i$ 

Por fim temos: $V_f = \frac{2M - M - m}{M+m}V_i + \frac{m-M + M+m}{M+m}v_i$ $\implies$ $V_f = \frac{M-m}{M+m}V_i + \frac{2m}{M+m}v_i$

Concluindo:

$v_f = \frac{2M}{M+m}V_i + \frac{m-M}{M+m}v_i$

$V_f = \frac{M-m}{M+m}V_i + \frac{2m}{M+m}v_i$







    
