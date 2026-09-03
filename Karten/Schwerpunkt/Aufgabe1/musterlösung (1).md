Gesucht sind die Schwerpunktkoordinaten $x_s$ und $y_s$ eines Kreisausschnitts mit Radius $r$ und Öffnungswinkel $2\alpha$.

Zur Beschreibung der Fläche werden Polarkoordinaten $\rho$ und $\varphi$ verwendet. Der Winkel $\varphi$ wird von der $y$-Achse aus gemessen und läuft von $-\alpha$ bis $+\alpha$, die Radialkoordinate $\rho$ vom Mittelpunkt bis zum Kreisbogen:

$$-\alpha \le \varphi \le \alpha, \qquad 0 \le \rho \le r$$

Da der Kreisausschnitt symmetrisch zur $y$-Achse liegt, folgt sofort:

$$x_s = 0$$

Das Flächenelement und die $y$-Koordinate eines Punktes lauten in diesen Koordinaten:

$$\mathrm{d}A = \rho\,\mathrm{d}\rho\,\mathrm{d}\varphi, \qquad y = \rho\cos\varphi$$

Integration über $\rho$ und $\varphi$ liefert die Gesamtfläche:

$$A = \int_{-\alpha}^{\alpha}\int_0^r \rho\,\mathrm{d}\rho\,\mathrm{d}\varphi = \alpha r^2$$

Analog ergibt sich das statische Moment bezüglich der $x$-Achse:

$$S_x = \int_{-\alpha}^{\alpha}\int_0^r \rho\cos\varphi\cdot\rho\,\mathrm{d}\rho\,\mathrm{d}\varphi = \frac{r^3}{3}\big[\sin\varphi\big]_{-\alpha}^{\alpha} = \frac{2r^3\sin\alpha}{3}$$

Der Schwerpunkt ist definiert als Quotient aus statischem Moment und Fläche:

$$y_s = \frac{S_x}{A} = \frac{\frac{2r^3\sin\alpha}{3}}{\alpha r^2} = \frac{2}{3}\,r\,\frac{\sin\alpha}{\alpha}$$

Die gesuchten Schwerpunktkoordinaten sind somit:

$$x_s = 0, \qquad y_s = \frac{2}{3}\,r\,\frac{\sin\alpha}{\alpha}$$

Als Kontrolle wird der Sonderfall $\alpha = \frac{\pi}{2}$ (Halbkreis) betrachtet:

$$y_s = \frac{2}{3}\,r\,\frac{\sin(\pi/2)}{\pi/2} = \frac{4r}{3\pi}$$

Dies entspricht der bekannten Schwerpunktlage des Halbkreises.
