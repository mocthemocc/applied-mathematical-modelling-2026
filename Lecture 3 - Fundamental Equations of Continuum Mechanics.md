# Lecture 3 — Fundamental Equations of Continuum Mechanics
**MATH3001(5005) — Applied Mathematical Modelling**
Prof. Benchawan Wiwatanapataphee, Curtin University — 4 Jul 2026

---

## Table of Contents
0. Introduction to Continuum Mechanics
1. Stress and Stress Equations of Motion
   1.1 Stress Components, Notation
   1.2 Sign Convention
   1.3 Stress Relations at a Point
   1.4 Principal Stresses
   1.5 Stress Equations of Motion
2. Strain and Geometric Equations
3. The Continuity Equation
4. Constitutive Equations
   4.1 Newtonian Fluid
   4.2 Hookean Elastic Solid
5. How It All Fits Together

---

## 0. Introduction to Continuum Mechanics

### Particle mechanics vs. continuum mechanics

| | Particle Mechanics | Continuum Mechanics |
|---|---|---|
| Idealisation | Object idealised as a **particle** | Material occupies **continuous space** |
| Properties | Has mass but no size or shape | Internal points move and deform |
| Governing law | Motion described by **Newton's laws** | Interested in deformation, stress, and possible failure |

**What is a continuum?** A continuum is an idealisation in which:
- mass is continuously distributed throughout a body,
- material properties vary continuously,
- deformation occurs under applied forces.

This assumption lets us describe materials using **fields** (e.g. displacement, stress, density) instead of tracking individual particles/molecules — this is what makes calculus-based modelling of solids and fluids possible.

**What is continuum mechanics?** It studies the behaviour of materials in **space and time**. This includes motion, deformation, stress, and failure, together with the effects of external forces and body forces.

### Branches

Continuum mechanics splits into two branches:
- **Solid Mechanics**
- **Fluid Mechanics**

Physical quantities of interest across both branches include: velocity, strain, stress, temperature, and density.

### The Four Fundamental Ingredients

Every continuum mechanics model is built from four pieces, which map directly onto the four sections of this lecture:

1. **Stress** — equations of motion (momentum balance)
2. **Strain** — geometric relations (how displacement produces deformation)
3. **Continuity equation** — conservation of mass
4. **Constitutive equations** — material behaviour (how stress relates to strain/strain-rate)

Sections 1–3 come from universal physics (Newton's laws + mass conservation) and apply to *any* continuum. Section 4 is where you plug in *which material* you're modelling.

---

## 1. Stress and Stress Equations of Motion

### Motivation: the traction vector

Consider a body Ω subjected to external loading (forces $F_1, F_2, F_3, F_4$ acting on it). Imagine an internal surface $S$ passing through a point $P$. Cutting along $S$ conceptually separates the body into two parts, $\Omega_a$ and $\Omega_b$. One part exerts an **internal force** $\Delta F$ on the other, across a small surface element $\Delta A$ with unit outward normal $\hat n$.

For a small surface element $\Delta A$, the force per unit area is called the **traction (stress) vector**:

$$\mathbf t(\hat n) = \lim_{\Delta A \to 0} \frac{\Delta F}{\Delta A}$$

**Key idea:** Stress measures *force intensity* (force per unit area), not total force.

**Crucial remark:** The traction vector $\mathbf t(\hat n)$ depends on the *orientation* of the surface through the unit normal $\hat n$ — different planes through the *same point* generally carry *different* traction vectors. This is precisely why we need a whole tensor (not just a vector) to describe the stress state at a point — see §1.3.

### 1.1 Stress Components and Notation

The stress vector is generally **not perpendicular** to the surface it acts on, and can be resolved into:
- one **normal** component, associated with tension or compression,
- two **shear** components, associated with change of shape,

with respect to the orthonormal basis $(\hat n, \mathbf s_1, \mathbf s_2)$ where $\hat n$ is the unit normal to the surface and $\mathbf s_1, \mathbf s_2$ are mutually orthogonal tangent vectors. The corresponding stress components are:

**Normal stress:** $\sigma_n$  **Shear stresses:** $\sigma_{s1}, \sigma_{s2}$

$$\mathbf t(\hat n) = \sigma_n \hat n + \sigma_{s1}\mathbf s_1 + \sigma_{s2}\mathbf s_2$$

Formally, resolving $\Delta \mathbf F$ into normal and tangential components:

$$\sigma_n = \lim_{\Delta A\to 0}\frac{\Delta F_n}{\Delta A}, \qquad \sigma_{s1}=\lim_{\Delta A\to 0}\frac{\Delta F_{s1}}{\Delta A}, \qquad \sigma_{s2}=\lim_{\Delta A\to 0}\frac{\Delta F_{s2}}{\Delta A}$$

**Index notation (the general 3D picture).** Consider a cube of material with sides parallel to the coordinate planes. The stress components are denoted $\sigma_{ij}$, where:
- the **first subscript** $i$ identifies the plane whose outward normal is in the $x_i$ direction,
- the **second subscript** $j$ identifies the direction in which the stress component acts.

For each coordinate plane:

| Plane | Stress components |
|---|---|
| $x_1$-plane | $\sigma_{11}, \sigma_{12}, \sigma_{13}$ |
| $x_2$-plane | $\sigma_{21}, \sigma_{22}, \sigma_{23}$ |
| $x_3$-plane | $\sigma_{31}, \sigma_{32}, \sigma_{33}$ |

This gives the full **3×3 stress tensor**:

$$[\sigma_{ij}] = \begin{pmatrix}\sigma_{11}&\sigma_{12}&\sigma_{13}\\ \sigma_{21}&\sigma_{22}&\sigma_{23}\\ \sigma_{31}&\sigma_{32}&\sigma_{33}\end{pmatrix}$$

#### Worked Example — Stress Notation

Given the stress tensor at a point in a 3D material:

$$[\sigma_{ij}] = \begin{pmatrix}80&25&-10\\25&50&15\\-10&15&30\end{pmatrix}\ \text{MPa}$$

- **On the $x_1$-plane** (outward normal $\parallel x_1$-axis), take the first row:
  $$\mathbf t^{(1)}=\begin{pmatrix}\sigma_{11}\\\sigma_{12}\\\sigma_{13}\end{pmatrix}=\begin{pmatrix}80\\25\\-10\end{pmatrix}\text{MPa}$$
  Here $\sigma_{11}$ is the **normal stress** on the $x_1$-plane; $\sigma_{12}$ is the **shear stress acting in the $x_2$ direction**; $\sigma_{13}$ is the shear stress acting in the **negative** $x_3$ direction (because its value, $-10$, is negative).

- **On the $x_2$-plane**, take the second row:
  $$\mathbf t^{(2)}=\begin{pmatrix}25\\50\\15\end{pmatrix}\text{MPa}$$
  $\sigma_{22}$ = normal stress; $\sigma_{21}$ = shear in $x_1$ direction; $\sigma_{23}$ = shear in $x_3$ direction.

- **On the $x_3$-plane**, take the third row:
  $$\mathbf t^{(3)}=\begin{pmatrix}-10\\15\\30\end{pmatrix}\text{MPa}$$
  $\sigma_{33}$ = normal stress; $\sigma_{31}$ = shear in the **negative** $x_1$ direction; $\sigma_{32}$ = shear in $x_2$ direction.

**Summary table:**

| Plane | Normal stress | First shear stress | Second shear stress |
|---|---|---|---|
| $x_1$-plane | $\sigma_{11}=80$ MPa | $\sigma_{12}=25$ MPa | $\sigma_{13}=-10$ MPa |
| $x_2$-plane | $\sigma_{22}=50$ MPa | $\sigma_{21}=25$ MPa | $\sigma_{23}=15$ MPa |
| $x_3$-plane | $\sigma_{33}=30$ MPa | $\sigma_{31}=-10$ MPa | $\sigma_{32}=15$ MPa |

### Symmetry of the Stress Tensor

For a material in **static equilibrium without body couples**, the stress tensor is **symmetric**:

$$\sigma_{ij}=\sigma_{ji}$$

(This is not just asserted — it is *proved* in §1.5 via moment balance on a differential element.) In the worked example above, $\sigma_{12}=\sigma_{21}=25$, $\sigma_{13}=\sigma_{31}=-10$, $\sigma_{23}=\sigma_{32}=15$ — consistent with symmetry.

**Consequence:** although the stress tensor has 9 components, only **6 are independent**: $\sigma_{11}, \sigma_{22}, \sigma_{33}, \sigma_{12}, \sigma_{13}, \sigma_{23}$.

### 1.2 Sign Convention

**General rule.** A stress component $\sigma_{ij}$ is taken as **positive** if:
- it acts on a **positive** $x_i$-plane in the **positive** $x_j$ direction, **or**
- it acts on a **negative** $x_i$-plane in the **negative** $x_j$ direction.

A **negative** stress component acts in the direction *opposite* to the positive sign convention.

Equivalently: if a stress component $\sigma_{ij}$ has a positive value, then it acts in the direction shown in the standard convention diagram; otherwise it acts in the opposite direction.

#### Worked Example — Sign Convention

Consider a cubic element with $\sigma_{11}=60$ MPa, $\sigma_{22}=-25$ MPa, $\sigma_{12}=18$ MPa, $\sigma_{13}=-10$ MPa. (Recall: first subscript = plane, second subscript = direction.)

- **$\sigma_{11}=+60$ MPa** (positive normal stress): on the positive $x_1$-plane it acts in the positive $x_1$ direction; on the negative $x_1$-plane it acts in the negative $x_1$ direction. → $\sigma_{11}$ represents a **tensile** normal stress.
- **$\sigma_{22}=-25$ MPa** (negative normal stress): on the positive $x_2$-plane it acts in the negative $x_2$ direction; on the negative $x_2$-plane it acts in the positive $x_2$ direction. → $\sigma_{22}$ represents a **compressive** normal stress.
- **$\sigma_{12}=+18$ MPa** (positive shear): first subscript ($1$) → acts on $x_1$-plane; second subscript ($2$) → acts in $x_2$ direction. Positive means: on the positive $x_1$-plane, acts in the positive $x_2$ direction; on the negative $x_1$-plane, acts in the negative $x_2$ direction.
- **$\sigma_{13}=-10$ MPa** (negative shear): on the positive $x_1$-plane it acts in the negative $x_3$ direction; on the negative $x_1$-plane it acts in the positive $x_3$ direction.

**Summary table:**

| Stress component | Plane | Direction | Sign interpretation |
|---|---|---|---|
| $\sigma_{11}=+60$ MPa | $x_1$-plane | $x_1$ direction | Tensile normal stress |
| $\sigma_{22}=-25$ MPa | $x_2$-plane | $x_2$ direction | Compressive normal stress |
| $\sigma_{12}=+18$ MPa | $x_1$-plane | $x_2$ direction | Positive shear stress |
| $\sigma_{13}=-10$ MPa | $x_1$-plane | $x_3$ direction | Negative shear stress |

### 1.3 Stress Relations at a Point (Cauchy's Formula — 2D derivation)

**The problem.** Different planes passing through the same point generally carry *different* traction vectors (as noted above). So: *if the stresses on the coordinate planes are known, can we determine the stress on any other plane?* The answer is **yes**, and the relationship is derived below by balancing forces on a small triangular ("wedge") element.

**Setup.** Consider a differential triangular element with legs $dx_1, dx_2$ and hypotenuse of length $ds$, inclined at angle $\theta$. The inclined face has:
- unit normal $\hat n$, unit tangent $\hat s$,
- normal stress $\sigma_n$ and shear stress $\tau_n$ (or $\sigma_{ns}$) acting on it,
- the coordinate faces carry the known stresses $\sigma_{11}, \sigma_{12}, \sigma_{21}, \sigma_{22}$.

From the geometry:

$$\hat{\mathbf s} = (s_1,s_2) = (\cos\theta,\sin\theta), \qquad \hat{\mathbf n}=(n_1,n_2)=(-\sin\theta,\cos\theta)$$

The side lengths satisfy:

$$dx_1 = ds\cos\theta = n_2\,ds, \qquad dx_2 = ds\sin\theta = -n_1\,ds \qquad \text{(1)}$$

**Force balance in the normal direction.** Applying Newton's 2nd law, $\sum F_n = m a_n$:

$$\sigma_{nn}\,ds + (\sigma_{11},\sigma_{12})\cdot\mathbf n\,dx_2 + (-\sigma_{21},-\sigma_{22})\cdot\mathbf n\,dx_1 = \rho\,dx_1 dx_2\,a_n/2$$

Substituting Equation (1):

$$\sigma_{nn}\,ds - \sigma_{1j}n_j n_1\,ds - \sigma_{2j}n_j n_2\,ds = -\rho\,n_1 n_2 (ds)^2 a_n/2$$
$$\sigma_{nn} - \sigma_{1j}n_j n_1 - \sigma_{2j}n_j n_2 = -\rho\,n_1 n_2\,ds\,a_n/2$$

**Taking the limit $ds \to 0$** (the inertia term vanishes as it is $O(ds)$ smaller):

$$\boxed{\sigma_{nn} = \sigma_{ij}n_j n_i} \qquad \text{(2)}$$

Similarly, from $\sum F_s = m a_s$ (balance in the tangential direction):

$$\boxed{\sigma_{ns} = \sigma_{ij}s_j n_i} \qquad \text{(3)}$$

**This is Cauchy's stress theorem in disguise** — it shows that the traction on *any* plane through a point can be computed from the *six* independent stress-tensor components on the coordinate planes; you don't need to know the stress on every possible orientation separately.

**In terms of the angle $\theta$**, Equations (2) and (3) become:

$$\boxed{\sigma_{nn}=\sigma_{11}\sin^2\theta+\sigma_{22}\cos^2\theta-(\sigma_{12}+\sigma_{21})\sin\theta\cos\theta} \qquad \text{(4)}$$
$$\boxed{\sigma_{ns}=(\sigma_{22}-\sigma_{11})\sin\theta\cos\theta-\sigma_{12}\sin^2\theta+\sigma_{21}\cos^2\theta} \qquad \text{(5)}$$

These are the classical **stress transformation equations** (the basis of Mohr's circle).

**Matrix forms.**

2-D: $\begin{pmatrix}\sigma_{11}&\sigma_{12}\\\sigma_{21}&\sigma_{22}\end{pmatrix}$   3-D: $\begin{pmatrix}\sigma_{11}&\sigma_{12}&\sigma_{13}\\\sigma_{21}&\sigma_{22}&\sigma_{23}\\\sigma_{31}&\sigma_{32}&\sigma_{33}\end{pmatrix}$

The stress components are **not all independent**. In the absence of couple stresses, the stress tensor is symmetric, $\sigma_{ij}=\sigma_{ji}$ ($i,j=1,2,3$). For the 2-D case with symmetry imposed, only three independent components remain: $\begin{pmatrix}\sigma_{11}&\sigma_{12}\\\sigma_{12}&\sigma_{22}\end{pmatrix}$.

### 1.4 Principal Stresses

**The question.** The normal stress $\sigma_{nn}$ on the $n$-plane depends on the angle $\theta$ (Equation 4). *Which plane carries the maximum normal stress? Which carries the minimum?* The planes where this extremum occurs are called the **principal planes**, and the corresponding normal stresses are the **principal stresses**.

Because $\sigma_{nn}(\theta)$ from Eq. (4) is periodic, there are exactly two mutually perpendicular principal planes at angles $\theta_1$ and $\theta_2=\theta_1+\pi/2$ (this periodicity of $\tan 2\theta$ is what forces the two extremal planes to be $90°$ apart).

**Derivation.** The principal planes are found by setting $d\sigma_{nn}/d\theta=0$:

$$\frac{d\sigma_{nn}}{d\theta}=2\sigma_{11}\sin\theta\cos\theta-2\sigma_{22}\sin\theta\cos\theta-2\sigma_{12}\cos2\theta=0$$

This gives:

$$\boxed{\tan 2\theta = \frac{2\sigma_{12}}{\sigma_{11}-\sigma_{22}}}$$

Hence the two principal planes are oriented at angles:

$$\theta_1=\frac12\arctan\!\left(\frac{2\sigma_{12}}{\sigma_{11}-\sigma_{22}}\right), \qquad \theta_2=\theta_1+\frac{\pi}{2}, \qquad \theta_1\perp\theta_2$$

**The corresponding principal stresses (eigenvalues of the stress tensor) are:**

$$\boxed{\sigma_{1,2} = \frac{\sigma_{11}+\sigma_{22}}{2}\pm\left[\left(\frac{\sigma_{11}-\sigma_{22}}{2}\right)^2+\sigma_{12}^2\right]^{1/2}}$$

where:
- $R=\left[\left(\dfrac{\sigma_{11}-\sigma_{22}}{2}\right)^2+\sigma_{12}^2\right]^{1/2}$ is the **radius of Mohr's Circle**,
- $\sigma_{\text{avg}}=\dfrac{\sigma_{11}+\sigma_{22}}{2}$ is the **average normal stress** (the centre of Mohr's circle).

So $\sigma_1=\sigma_{\text{avg}}+R$ (maximum principal stress), $\sigma_2=\sigma_{\text{avg}}-R$ (minimum principal stress).

#### Worked Example — 2-D Stress Analysis

At a point in a 2-D stress field: $\sigma_x=2$ MPa, $\sigma_y=8$ MPa, $\tau_{xy}=4$ MPa (positive shear acts upward on the +x face and rightward on the +y face).

**(a) Principal stresses and directions.**

*Step 1 — average normal stress:*
$$\sigma_{\text{avg}}=\frac{\sigma_x+\sigma_y}{2}=\frac{2+8}{2}=5\text{ MPa}$$

*Step 2 — Mohr's circle radius:*
$$R=\sqrt{\left(\frac{\sigma_x-\sigma_y}{2}\right)^2+\tau_{xy}^2}=\sqrt{\left(\frac{2-8}{2}\right)^2+4^2}=\sqrt{9+16}=5\text{ MPa}$$

*Step 3 — principal stresses:*
$$\sigma_1=\sigma_{\text{avg}}+R=5+5=10\text{ MPa}\qquad(\text{maximum})$$
$$\sigma_2=\sigma_{\text{avg}}-R=5-5=0\text{ MPa}\qquad(\text{minimum})$$

*Principal directions:*
$$\tan(2\theta_p)=\frac{2\tau_{xy}}{\sigma_x-\sigma_y}=\frac{2(4)}{2-8}=-\frac43 \;\Rightarrow\; 2\theta_p=126.87° \;\Rightarrow\; \theta_{p1}=63.43°$$
$$\theta_{p2}=\theta_{p1}+90°=153.43°\quad(\text{or equivalently } -26.57°)$$

**Final answers for part (a):**

| Quantity | Value |
|---|---|
| Maximum principal stress $\sigma_1$ | **10 MPa** |
| Minimum principal stress $\sigma_2$ | **0 MPa** |
| Direction of $\sigma_1$ | **63.43° CCW from +x-axis** |
| Direction of $\sigma_2$ | **−26.57° (or 153.43°)** |

**(b) Maximum in-plane shear stress and orientation.**

The maximum in-plane shear stress equals the radius of Mohr's circle:
$$\tau_{\max}=R=5\text{ MPa}$$

The normal stress acting on the maximum-shear planes is the average normal stress:
$$\sigma_n=\sigma_{\text{avg}}=5\text{ MPa}$$

The maximum-shear planes occur $45°$ from the principal planes:
$$\theta_s=\theta_{p1}-45°=63.43°-45°=18.43°\qquad(\text{second plane: }108.43°)$$

**Final answers for part (b):**

| Quantity | Value |
|---|---|
| Maximum in-plane shear stress | **5 MPa** |
| Normal stress on shear planes | **5 MPa** |
| Shear plane orientations | **18.43° and 108.43°** |

**Key intuition to remember:** on the principal planes shear stress is zero and normal stress is extremal; on the maximum-shear planes (45° away), the normal stress is the *average* stress and the shear is extremal. This is exactly what a Mohr's circle diagram encodes geometrically (centre = $\sigma_{\text{avg}}$, radius = $R$, principal points on the horizontal axis, max-shear points at the top/bottom of the circle, $180°$ around the circle = $90°$ in real space).

### 1.5 Stress Equations of Motion (Cauchy's Equation of Motion)

Stress equations of motion describe how stress **gradients** and **body forces** produce **acceleration**. This is simply Newton's second law ($F=ma$) applied to a continuum.

**Newton's second law for a continuum gives:**

$$\boxed{\frac{\partial \sigma_{ji}}{\partial x_j}+\rho X_i=\rho a_i} \qquad \text{(6)}$$

where:
- $\rho$ is density,
- $X_i$ is body force per unit mass (e.g. gravity),
- $a_i$ is acceleration.

**Derivation (2-D, via a differential element).** Consider a differential rectangular element of sides $dx, dy$ with corners labelled $A,B,C,D$. By Taylor expansion (stress continuity), the forces on the far faces are related to those on the near faces:

$$\sigma_{xx}(x+dx,y)=\sigma_{xx}(x,y)+\frac{\partial\sigma_{xx}}{\partial x}dx+O[(dx)^2]$$
$$\sigma_{xy}(x+dx,y)=\sigma_{xy}(x,y)+\frac{\partial\sigma_{xy}}{\partial x}dx+O[(dx)^2]$$

- Forces on plane $AB$ (bottom, at $y$): $\sigma_{yx}(x,y)$ and $\sigma_{yy}(x,y)$.
- Forces on plane $CD$ (top, at $y+dy$): $\sigma_{yx}(x,y+dy)$ and $\sigma_{yy}(x,y+dy)$.

Applying Newton's 2nd law in the $x$-direction, $\sum F_x = m a_x$, expanding via Taylor series and taking $dx,dy\to 0$, yields the **stress equation of motion in the $x$-direction**:

$$\frac{\partial\sigma_{xx}}{\partial x}+\frac{\partial\sigma_{yx}}{\partial y}+\rho X=\rho a_x$$

Similarly, in the $y$-direction:

$$\frac{\partial\sigma_{xy}}{\partial x}+\frac{\partial\sigma_{yy}}{\partial y}+\rho Y=\rho a_y$$

**Proof that the stress tensor is symmetric.** Further, applying **moment balance**, $\sum M_o = 0$, about the centre of the element: therefore, in the absence of couple stresses, the shear stresses on mutually perpendicular planes are equal:

$$\sigma_{xy}=\sigma_{yx}$$

which indicates that the stress tensor is a **second-order symmetric tensor**. (This is the promised proof referenced back in §1.1 — symmetry isn't an assumption, it *follows* from angular momentum balance.)

**Special case — incompressible material.** (Preview, connects to §3): if the material is incompressible, the continuity equation forces $v_{i,i}=0$; this is used together with Eq. (6) in the Newtonian-fluid constitutive law (§4.1).

---

## 2. Strain and Geometric Equations

When external forces act on a body, material points are displaced and the body may change both **size** and **shape**. These effects are measured by the **strain components**.

### Setup

Consider a 2-D displacement field:
$$u=u(x,y,t), \qquad v=v(x,y,t)$$
where $u$ and $v$ are the displacements in the $x$- and $y$-directions respectively.

Consider a small rectangular element $ABDA$ (with $A$ at the origin corner) that deforms into $A'B'D'$. $AB$ and $AD$ deform into $A'B'$ and $A'D'$. The displacements of point $A$ are $u_A$ and $v_A$.

**Displacement of point $B$** (a distance $dx$ from $A$ along $x$), by the continuum (Taylor-expansion) assumption:

$$u_B = u(x+dx,y,t) = u(x,y,t)+\frac{\partial u}{\partial x}dx = u_A+\frac{\partial u}{\partial x}dx, \qquad v_B = v_A+\frac{\partial v}{\partial x}dx$$

**Displacement of point $D$** (a distance $dy$ from $A$ along $y$):

$$u_D = u(x,y+dy,t) = u_A + \frac{\partial u}{\partial y}dy, \qquad v_D = v_A+\frac{\partial v}{\partial y}dy$$

### Normal strain (change in size)

Since the rotation angle $d\beta$ is small, the **stretch** of the line $AB$ is:

$$\Delta(dx) = u_B - u_A = \frac{\partial u}{\partial x}dx$$

This motivates defining the **normal strain** as the *change in length per unit length*:

**2.1 Normal strain in the $x$-direction** — measures the change in length per unit length in the $x$-direction:

$$\boxed{\varepsilon_{xx}=\frac{\dfrac{\partial u}{\partial x}dx}{dx}=\frac{\partial u}{\partial x}} \qquad \text{(7)}$$

**Normal strain in the $y$-direction** — measures the change in length per unit length in the $y$-direction:

$$\boxed{\varepsilon_{yy}=\frac{\partial v}{\partial y}} \qquad \text{(8)}$$

### Shear strain (change in shape)

**2.2 Shear strain** — measures the change in angle from the original right angle at point $A$ (i.e. how much the originally perpendicular edges $AB$ and $AD$ rotate towards/away from each other):

$$\gamma_{xy}=d\theta+d\beta = \frac{\partial u}{\partial y}+\frac{\partial v}{\partial x}=2\varepsilon_{xy} \qquad \text{(9)}$$

So the *tensorial* shear strain $\varepsilon_{xy}$ is **half** the *engineering* shear strain $\gamma_{xy}$.

**Interpretation:**
- **Normal strains measure change in size.**
- **Shear strains measure change in shape.**

### 2.3 Geometric Equations (General Strain–Displacement Relation)

The strain–displacement relations Equation (7)–Equation (9) can be expressed in general **index notation** as:

$$\boxed{\varepsilon_{ij}=\frac12\left(\frac{\partial u_i}{\partial x_j}+\frac{\partial u_j}{\partial x_i}\right)} \qquad \text{(10)}$$

This is the **infinitesimal (small) strain tensor** — the symmetric part of the displacement-gradient tensor. Strain components are determined from the displacement field by this kinematic (purely geometric) equation — note it involves **no physics**, only geometry: it is true regardless of what material you're dealing with.

---

## 3. The Continuity Equation

The continuity equation expresses **conservation of mass**. Since mass can neither be created nor destroyed, the density $\rho$ and velocity $\mathbf v$ fields in a continuum satisfy:

$$\boxed{\frac{\partial\rho}{\partial t}+\text{div}(\rho\mathbf v)=0}$$

### Derivation (control-volume argument)

Consider a **fixed control volume** $\Omega$ with closed boundary surface $S$ and outward unit normal $\mathbf n$. If the fluid velocity is $\mathbf v$, the outward normal component of velocity is:

$$v_n=\mathbf v\cdot\mathbf n$$

Let $dS$ be a differential surface element (on $S$) with area $dS$, and let $dl$ be a differential length in the $\mathbf n$ direction (the distance the fluid moves in unit time):

$$dl=\mathbf v\cdot\mathbf n = v_n$$

The volume of fluid flowing out of $\Omega$ through $dS$ is the volume of the thin cylinder with cross-section area $dS$ and length $dl=v_n$:

$$dV=v_n\,dS$$

The **mass flow rate** out through $dS$ is therefore:

$$dQ=\rho v_n\,dS=\rho\,\mathbf v\cdot\mathbf n\,dS$$

so the **total mass efflux** (integrating over the whole boundary $S$) is:

$$Q=\iint_S \rho\,\mathbf v\cdot\mathbf n\,dS \qquad \text{(11)}$$

**The rate of decrease of mass within $\Omega$** is:

$$-\iiint_\Omega \frac{\partial\rho}{\partial t}\,d\Omega \qquad \text{(12)}$$

**Equating outflow with the rate of decrease of mass** (mass leaving = mass lost from the interior):

$$-\iiint_\Omega \frac{\partial\rho}{\partial t}\,d\Omega = \iint_S \rho\,\mathbf v\cdot\mathbf n\,dS \qquad \text{(13)}$$

**Applying the divergence theorem** to convert the surface integral to a volume integral:

$$\iint_S \rho\,\mathbf v\cdot\mathbf n\,dS = \iiint_\Omega \text{div}(\rho\mathbf v)\,d\Omega$$

Substituting into (13):

$$-\iiint_\Omega \frac{\partial\rho}{\partial t}\,d\Omega = \iiint_\Omega \text{div}(\rho\mathbf v)\,d\Omega$$

**Since $\Omega$ is arbitrary** (this control volume could be *any* region inside the material), the integrands themselves must be equal, giving the **differential form**:

$$\boxed{\frac{\partial\rho}{\partial t}+\text{div}(\rho\mathbf v)=0}$$

### Special case — incompressible material

For an incompressible material, $\partial\rho/\partial t = 0$ (density of a fluid particle doesn't change), so the continuity equation reduces to:

$$\boxed{v_{i,i}=0} \qquad \text{(i.e. } \text{div}(\mathbf v)=0\text{)}$$

This is the **incompressibility condition** used constantly in fluid mechanics (e.g. Navier–Stokes for incompressible flow) — it says the velocity field must be divergence-free.

---

## 4. Constitutive Equations

The equations developed so far describe:
- **conservation of momentum** (§1 — the stress equations of motion),
- **geometry** (§2 — strain–displacement relations),
- **conservation of mass** (§3 — the continuity equation).

**However, they do not describe how a material responds to deformation.** These three sets of equations are *universal* — true for water, steel, rubber, air, everything — precisely because they encode only physics (Newton's laws, mass conservation) and geometry (how strain relates to displacement), not material identity. To close the system, we need one more ingredient: a **constitutive equation**.

A constitutive equation relates **stress** to the material response:

$$\sigma_{ij}=f_{ij}(\text{history of deformation},\ \text{history of temperature})$$

> **Note.** Different materials require different constitutive laws. This is the "personality" of the material in the model — everything else in continuum mechanics is generic.

Two important **idealised linear models** are:
- **Newtonian fluid**
- **Hookean elastic solid**

### 4.1 Newtonian Fluid

> A **Newtonian fluid** is a fluid whose viscous stress is **linearly proportional to the rate of deformation**. Equivalently, its **viscosity remains constant** and is independent of the rate of deformation (or shear rate).

For an **isotropic** Newtonian fluid, the constitutive equation is:

$$\boxed{\sigma_{ij}=-p\delta_{ij}+\lambda d_{kk}\delta_{ij}+2\mu d_{ij}} \qquad \text{(14)}$$

where:
- $d_{ij}=\dfrac12(v_{i,j}+v_{j,i})$ is the **rate-of-deformation tensor** (or strain-rate tensor) — note the structural parallel with $\varepsilon_{ij}$ in Eq. (10), but built from *velocity* gradients instead of *displacement* gradients,
- $p$ is the **thermodynamic pressure**,
- $\mu$ is the **dynamic viscosity**,
- $\lambda$ is the **second coefficient of viscosity** (second viscosity).

**Interpretation:** the first term ($-p\delta_{ij}$) represents the **isotropic pressure**, while the remaining terms describe the **viscous stresses** generated by fluid deformation.

**Incompressible case.** For incompressible fluids, $d_{kk}=0$ (matches the continuity-equation result from §3), so the constitutive equation simplifies to:

$$\boxed{\sigma_{ij}=-p\delta_{ij}+2\mu d_{ij}}$$

In **component form** (the version you'll actually use in calculations / the Navier–Stokes equations):

$$\sigma_{xx}=-p+2\mu\frac{\partial u}{\partial x},\quad \sigma_{yy}=-p+2\mu\frac{\partial v}{\partial y},\quad \sigma_{zz}=-p+2\mu\frac{\partial w}{\partial z}$$
$$\sigma_{xy}=\mu\left(\frac{\partial u}{\partial y}+\frac{\partial v}{\partial x}\right),\quad \sigma_{yz}=\mu\left(\frac{\partial v}{\partial z}+\frac{\partial w}{\partial y}\right),\quad \sigma_{zx}=\mu\left(\frac{\partial w}{\partial x}+\frac{\partial u}{\partial z}\right)$$

**Examples:**
- **Newtonian fluids:** water, air, and most common gases.
- **Non-Newtonian fluids:** ketchup, toothpaste, paint, and blood. A non-Newtonian fluid requires a more complex constitutive model, as its viscosity changes depending on the force or pressure applied.

### 4.2 Hookean Elastic Solid

> A **Hookean elastic solid** is a material for which the stress is **linearly proportional to the strain**. The material returns to its original shape after the load is removed, provided the deformation remains within the elastic limit.

The **general linear constitutive equation** (generalised Hooke's Law) is:

$$\sigma_{ij}=C_{ijkl}\varepsilon_{kl}$$

where $C_{ijkl}$ is the **fourth-order elastic stiffness tensor** that characterises the material (in general, anisotropic materials can have up to 21 independent constants here).

For an **isotropic** elastic solid, Hooke's law reduces to:

$$\boxed{\sigma_{ij}=\lambda\varepsilon_{kk}\delta_{ij}+2\mu\varepsilon_{ij}}$$

where:
- $\lambda$ and $\mu$ are the **Lamé constants**,
- $\mu$ is also known as the **shear modulus**.

**Notice the structural symmetry with the Newtonian fluid law (Eq. 14):** stress = (volumetric term)·$\delta_{ij}$ + 2·(coefficient)·(deformation tensor). The fluid law uses the **rate**-of-deformation tensor $d_{ij}$ (built from velocity gradients); the solid law uses the **strain** tensor $\varepsilon_{ij}$ (built from displacement gradients). This is a genuinely elegant parallel: an elastic solid "remembers" total deformation, while a viscous fluid only "feels" the rate of deformation.

**In particular** (component form):

$$\sigma_{xx}=\lambda(\varepsilon_{xx}+\varepsilon_{yy}+\varepsilon_{zz})+2\mu\varepsilon_{xx}, \qquad \sigma_{xy}=2\mu\varepsilon_{xy}$$

and similarly for the remaining stress components.

**Examples:**
- **Hookean solids:** steel, aluminum, and most metals under small deformations.
- **Non-Hookean solids:** rubber, polymers, and biological tissues. A non-Hookean solid requires a more complex constitutive model because its stress–strain relationship may be **nonlinear**, **time-dependent (viscoelastic)**, or both.

---

## 5. How It All Fits Together

This is the big picture that ties the whole lecture together — the **closed system of governing equations** for a deformable continuum:

1. **Kinematics (geometry):** $\varepsilon_{ij}=\frac12(u_{i,j}+u_{j,i})$ — relates strain to displacement. (6 equations, but derivable from 3 displacement components, so really 3 independent unknowns: $u,v,w$.)
2. **Kinetics (physics):** $\sigma_{ji,j}+\rho X_i=\rho a_i$ — Newton's second law for a continuum (3 equations, in 6 independent stress unknowns since $\sigma_{ij}=\sigma_{ji}$).
3. **Mass conservation:** $\partial\rho/\partial t+\text{div}(\rho\mathbf v)=0$ — 1 equation.
4. **Constitutive law:** $\sigma_{ij}=f_{ij}(\ldots)$ — closes the system by relating stress to strain/strain-rate (however many equations needed to match the unknowns, e.g. 6 for isotropic linear elasticity).

Without the constitutive equation, you have more unknowns (displacements, stresses, strains, density) than equations — the system is **not closed**. The constitutive law is what turns "generic continuum mechanics" into "the mechanics of *this specific* material" (steel vs. water vs. rubber), and this is exactly the missing piece that lets you go from the abstract balance laws to a solvable boundary-value problem (e.g. the Navier–Stokes equations for a Newtonian fluid, or the Navier–Cauchy / linear elasticity equations for a Hookean solid).

**Why this matters for a modelling project:** whenever you build a PDE model of a physical system (predator–prey included, by analogy — conservation laws + a constitutive/behavioural assumption closing the system), the same pattern repeats: (i) write down a *balance/conservation law* that must hold no matter what, (ii) write down the *geometric/kinematic relations* connecting your state variables, (iii) supply the *closure relation* (constitutive law / functional response / growth law) that encodes the specific behaviour of the system you're modelling.

---

## Quick-Reference Equation Sheet

| # | Equation | Meaning |
|---|---|---|
| — | $\mathbf t(\hat n)=\lim_{\Delta A\to0}\Delta F/\Delta A$ | Traction vector definition |
| — | $\mathbf t(\hat n)=\sigma_n\hat n+\sigma_{s1}\mathbf s_1+\sigma_{s2}\mathbf s_2$ | Normal/shear resolution |
| — | $\sigma_{ij}=\sigma_{ji}$ | Symmetry of stress tensor |
| (2) | $\sigma_{nn}=\sigma_{ij}n_jn_i$ | Cauchy's formula (normal stress on arbitrary plane) |
| (3) | $\sigma_{ns}=\sigma_{ij}s_jn_i$ | Cauchy's formula (shear stress on arbitrary plane) |
| — | $\tan2\theta=\dfrac{2\sigma_{12}}{\sigma_{11}-\sigma_{22}}$ | Principal plane orientation |
| — | $\sigma_{1,2}=\sigma_{\text{avg}}\pm R$ | Principal stresses |
| (6) | $\sigma_{ji,j}+\rho X_i=\rho a_i$ | Cauchy's equation of motion |
| (7)–(8) | $\varepsilon_{xx}=\partial u/\partial x,\ \varepsilon_{yy}=\partial v/\partial y$ | Normal strains |
| (9) | $\gamma_{xy}=\partial u/\partial y+\partial v/\partial x=2\varepsilon_{xy}$ | Shear strain |
| (10) | $\varepsilon_{ij}=\frac12(u_{i,j}+u_{j,i})$ | General strain–displacement relation |
| — | $\partial\rho/\partial t+\text{div}(\rho\mathbf v)=0$ | Continuity equation |
| — | $v_{i,i}=0$ | Incompressibility condition |
| (14) | $\sigma_{ij}=-p\delta_{ij}+\lambda d_{kk}\delta_{ij}+2\mu d_{ij}$ | Newtonian fluid |
| — | $\sigma_{ij}=\lambda\varepsilon_{kk}\delta_{ij}+2\mu\varepsilon_{ij}$ | Isotropic Hookean solid |

---

*Notes compiled from Lecture 3 (46 slides), MATH3001 Applied Mathematical Modelling, Semester 2 2026, Curtin University.*
