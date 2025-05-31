Below is the complete, “from-raw-data-to-final-number” math in compact notation.
(Choose either **min–max** or **z-score** scaling; only one is active at a time.)

---

### 1 | Scale every raw driver to 0 – 1  

For category $c$ and driver $x\in\{\text{lead-time},\text{CV},\text{vendor-conc.},\text{DOS},\text{LPI}\}$:

#### (a) Min–max scaling  *(default)*

$$
s_{c,x}^{\text{min-max}}
  \;=\;
  \frac{x_{c}-\min_{k}(x_{k})}
       {\max_{k}(x_{k})-\min_{k}(x_{k})}
\tag{1}
$$

#### (b) Z-score scaling  *(optional)*

$$
s_{c,x}^{\text{z}}
  \;=\;
  \frac{x_{c}-\mu_{x}}{\sigma_{x}}
\quad
\Bigl(
  \mu_{x} = \tfrac{1}{N}\sum_{k}x_{k},
  \;\sigma_{x} = \sqrt{\tfrac{1}{N}\sum_{k}(x_{k}-\mu_{x})^{2}}
\Bigr)
\tag{2}
$$

*(The code picks one of (1) or (2) via `config.SCALING`.)*

---

### 2 | Build the **internal** composite

Weights

$$
w_{\text{LT}}=0.40,\;w_{\text{CV}}=0.20,\;
w_{\text{VC}}=0.20,\;w_{\text{DOS}}=0.20
$$

$$
\boxed{
  I_{c}
  \;=\;
  w_{\text{LT}}\;s_{c,\text{LT}}
  \;+\;
  w_{\text{CV}}\;s_{c,\text{CV}}
  \;+\;
  w_{\text{VC}}\;s_{c,\text{VC}}
  \;+\;
  w_{\text{DOS}}\;s_{c,\text{DOS}}
}
\tag{3}
$$

---

### 3 | Build the **external** composite

Weights

$$
w_{\text{LOG}}=0.50,\quad
w_{\text{US}} =0.30,
\quad\bigl(\,w_{\text{tariff}}=0.20\text{ if added later}\bigr)
$$

Scaled logistics “badness” is inverted:

$$
s_{c,\text{LOG}} = 1 - s_{c,\text{LPI}}
$$

$$
\boxed{
  E_{c}
  \;=\;
  w_{\text{LOG}}\;s_{c,\text{LOG}}
  \;+\;
  w_{\text{US}}\;d_{c,\text{US}}
}
\tag{4}
$$

where $d_{c,\text{US}}\in[0,1]$ is the U.S.-vendor share.

---

### 4 | Raw (“base”) risk score

$$
\boxed{
  R^{\text{base}}_{c}
  \;=\;
  \tfrac12\bigl(I_{c}+E_{c}\bigr)
}
\tag{5}
$$

---

### 5 | Risk-tolerance overlay

Multiplier

$$
m_{c}=
\begin{cases}
1.00 & \text{High tolerance}\\
0.85 & \text{Medium}\\
0.70 & \text{Low}
\end{cases}
$$

$$
\boxed{
  R^{\text{adj}}_{c}
  \;=\;
  R^{\text{base}}_{c}\times m_{c}
}
\tag{6}
$$

This is the **score you sort on in the base scenario.**

---

### 6 | Tariff-shock scenario (25 % duty on U.S. imports)

Define:

* Threshold $\theta = 0.50$ (50 % U.S. dependence).
* Bump factor $b = 1 + \dfrac{25}{100} = 1.25$.

Indicator

$$
\mathbf{1}_{c}
  \;=\;
  \begin{cases}
    1 & \text{if } d_{c,\text{US}} > \theta\\
    0 & \text{otherwise}
  \end{cases}
$$

Scenario score

$$
\boxed{
  R^{\text{tariff}}_{c}
  \;=\;
  R^{\text{adj}}_{c}
  \;+\;
  \bigl(d_{c,\text{US}}\times(b-1)\bigr)
  \;\mathbf{1}_{c}
}
\tag{7}
$$

---

### 7 | Interpretation

* $R^{\text{adj}}_{c}\in[0,1]$ – deterministic *baseline* fragility.
* $R^{\text{tariff}}_{c}\ge R^{\text{adj}}_{c}$ – only categories above the U.S.-dependency threshold rise, and the rise is proportional to that dependency.
* You can treat equations (3)–(7) as a template: swap weights, thresholds, or add new terms (e.g., **tariff severity**, **port-closure probability**) without touching the rest of the pipeline.
