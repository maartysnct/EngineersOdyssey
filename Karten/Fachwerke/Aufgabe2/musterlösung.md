Gesucht sind die Stabkräfte $S_3$, $S_7$ und $S_8$ des dargestellten Fachwerks mit der Einzellast $F$ in Feldmitte.

Zunächst werden die Auflagerreaktionen bestimmt. Aus dem Momentengleichgewicht um das Lager $A$ folgt $B_v = \frac{1}{3}F$, und aus dem Momentengleichgewicht um $B$ folgt $A_v = \frac{2}{3}F$. Wegen fehlender horizontaler äußerer Kräfte ist $B_h = 0$.

$$A_v = \frac{2}{3}F, \qquad B_v = \frac{1}{3}F, \qquad B_h = 0$$

Im nächsten Schritt wird das Fachwerk freigeschnitten. Dabei sind die Auflagerkräfte und die Stabrichtungen zu berücksichtigen, damit die Gleichgewichtsbedingungen an den Knoten aufgestellt werden können.

Vor dem Rechnen lohnt sich die Identifikation der Nullstäbe. An unbelasteten Knoten, an denen zwei Stäbe kollinear liegen und ein dritter Stab senkrecht dazu angeschlossen ist, wirkt im dritten Stab keine Kraft. Damit ergeben sich:

$$S_4 = S_5 = S_9 = 0, \qquad S_{10} = S_{13} = 0$$

Nun werden die Gleichgewichtsbedingungen an den verbleibenden Knoten ausgewertet. Am linken oberen Knoten liefert das Kräftegleichgewicht in $z$-Richtung:

$$S_1 + A_v = 0 \quad \Rightarrow \quad S_1 = -\frac{2}{3}F$$

In $x$-Richtung ergibt sich:

$$S_1 + S_3\sin\alpha = 0 \quad \Rightarrow \quad S_3 = \frac{2\sqrt{5}}{3}F$$

Am Mittelknoten liefert die Gleichgewichtsbedingung in $z$-Richtung:

$$S_7\sin\alpha + S_3\sin\alpha = 0 \quad \Rightarrow \quad S_7 = -\frac{2\sqrt{5}}{3}F$$

Schließlich wird am rechten oberen Knoten das Gleichgewicht in $z$-Richtung betrachtet:

$$S_8 + S_7\cos\alpha - S_3\cos\alpha = 0 \quad \Rightarrow \quad S_8 = \frac{8}{3}F$$

Die gesuchten Stabkräfte sind somit:

$$S_3 = \frac{2\sqrt{5}}{3}F, \qquad S_7 = -\frac{2\sqrt{5}}{3}F, \qquad S_8 = \frac{8}{3}F$$

Negative Vorzeichen bedeuten Druckkräfte, positive Vorzeichen Zugkräfte.
