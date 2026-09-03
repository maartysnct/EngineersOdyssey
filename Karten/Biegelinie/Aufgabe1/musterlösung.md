**Aufgabe:** Bestimme $w(x)$ und $w(L)$ eines Kragarms ($EI=\text{const.}$) mit Endlast $F$. Zahlenwerte: $F=10\,\text{kN}$, $L=4\,\text{m}$.

1\. Koordinaten und Vorzeichen: $x$ vom Einspannende ($x=0$) nach rechts; $w$ nach oben positiv. $M$ positiv bei Zug am unteren Rand; Kragarm biegt sich abwärts, also $M(x)<0$.

2\. Auflagerreaktionen: $M_A=-FL$, $A_z=F$.

3\. Biegemoment: Schnitt am rechten Teil: $M(x)=-F(L-x)=-FL+Fx$.

4\. Biegelinien-DGL: $EI\,w''(x)=M(x)=-F(L-x)$.

5\. Erste Integration: $EI\,w'(x)=\int(-FL+Fx)\,dx=-FLx+\frac{F}{2}x^2+C_1$; aus $w'(0)=0$ folgt $C_1=0$.

$$\boxed{EI\,w'(x)=-FLx+\frac{F}{2}x^2}$$

6\. Zweite Integration: $EI\,w(x)=\int\!\left(-FLx+\frac{F}{2}x^2\right)dx=-\frac{FL}{2}x^2+\frac{F}{6}x^3+C_2$; aus $w(0)=0$ folgt $C_2=0$.

$$\boxed{w(x)=\frac{1}{EI}\left(-\frac{FL}{2}x^2+\frac{F}{6}x^3\right)}$$

7\. Maximale Durchbiegung: $w(L)=\frac{1}{EI}\left(-\frac{FL^3}{2}+\frac{FL^3}{6}\right)=-\frac{FL^3}{3EI}$.

$$\boxed{w(L)=-\frac{FL^3}{3EI}}$$

Für $F=10\,\text{kN}$ und $L=4\,\text{m}$: $w(L)=-\dfrac{640}{3EI}$.
