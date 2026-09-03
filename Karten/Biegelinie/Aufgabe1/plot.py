import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 3))

# Balken
ax.plot([0, 4], [0, 0], 'k-', lw=4)

# Lager A und B
ax.plot(0, 0, marker='^', markersize=12, color='black')
ax.plot(4, 0, marker='^', markersize=12, color='black')

# Boden unter den Lagern
ax.plot([-0.2, 0.2], [-0.18, -0.18], 'k-', lw=2)
ax.plot([3.8, 4.2], [-0.18, -0.18], 'k-', lw=2)

# Last F
ax.annotate(
    '',
    xy=(2, 0.02),
    xytext=(2, 0.7),
    arrowprops=dict(
        arrowstyle='->',
        color='firebrick',
        lw=2
    )
)
ax.text(
    2.08, 0.52,
    'F',
    color='firebrick',
    fontsize=14,
    fontweight='bold'
)

# z-Achse
ax.annotate(
    '',
    xy=(0, 0.75),
    xytext=(0, 0.05),
    arrowprops=dict(
        arrowstyle='->',
        color='teal',
        lw=2
    )
)
ax.text(
    -0.22, 0.78,
    'z',
    color='teal',
    fontsize=12,
    fontweight='bold'
)

# x-Achse
ax.annotate(
    '',
    xy=(0.85, -0.35),
    xytext=(0.05, -0.35),
    arrowprops=dict(
        arrowstyle='->',
        color='teal',
        lw=2
    )
)
ax.text(
    0.9, -0.4,
    'x',
    color='teal',
    fontsize=12,
    fontweight='bold'
)

# Momentenpfeil
ax.annotate(
    '',
    xy=(-0.45, 0.25),
    xytext=(-0.05, 0.05),
    arrowprops=dict(
        arrowstyle='->',
        color='teal',
        lw=2
    )
)
ax.text(
    -0.55, 0.28,
    'M',
    color='teal',
    fontsize=12,
    fontweight='bold'
)

# Textblock rechts
ax.text(4.55, 0.55, 'F = 10 kN', fontsize=13, fontweight='bold')
ax.text(4.55, 0.25, 'L = 4 m', fontsize=13, fontweight='bold')
ax.text(4.55, -0.05, r'$A_y = B_y$', fontsize=13, fontweight='bold')
ax.text(4.55, -0.35, r'$M_A = -40\,kNm$', fontsize=13, fontweight='bold')

ax.set_xlim(-0.8, 6.2)
ax.set_ylim(-0.7, 1.0)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.show()