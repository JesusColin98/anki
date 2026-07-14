import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # 01_Math_Foundations
    {
        "deck": "AI_Learning_Path::01_Classical_ML::01_Math_Foundations",
        "scenario": "ML Math: Singular Value Decomposition (SVD) 📊",
        "text": "For dimensionality reduction and matrix approximation, Singular Value Decomposition (SVD) factors a matrix A into U Sigma V^T where Sigma contains the {{c1::singular values}} in descending order and the columns of V represent the {{c2::right singular vectors (principal directions)}}.",
        "explanation": "SVD decomposition breaks down any real matrix into rotation (U), scaling (Sigma), and rotation (V^T) matrices. Truncating the singular values to the top k gives the best rank-k approximation of the matrix under the Frobenius norm (Eckart-Young-Mirsky theorem).",
        "usage": "Used in Principal Component Analysis (PCA) and collaborative filtering recommender systems.",
        "spanish": "Para la reducción de dimensionalidad y la aproximación de matrices, la Descomposición en Valores Singulares (SVD) factoriza una matriz A en U Sigma V^T, donde Sigma contiene los valores singulares en orden descendente y las columnas de V representan los vectores singulares derechos.",
        "tags": ["math", "svd", "linear_algebra"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::01_Math_Foundations",
        "scenario": "ML Math: MLE vs MAP Parameter Estimation 🧠",
        "text": "While Maximum Likelihood Estimation (MLE) maximizes the likelihood function P(D|theta), Maximum A Posteriori (MAP) estimation incorporates a prior distribution P(theta) by maximizing the product {{c1::P(D|theta)P(theta)}}.",
        "explanation": "MAP estimation computes the mode of the posterior distribution using Bayes' theorem. It acts as a bridge between frequentist and Bayesian inference, where the prior distribution P(theta) mathematically functions as a regularization term (e.g. Gaussian prior leads to L2 regularization).",
        "usage": "Core foundation for understanding regularization, bayesian classifiers, and parameter estimation.",
        "spanish": "Mientras que la Estimación de Máxima Verosimilitud (MLE) maximiza la función de verosimilitud P(D|theta), la Estimación Máxima a Posteriori (MAP) incorpora una distribución a priori P(theta) al maximizar el producto P(D|theta)P(theta).",
        "tags": ["math", "mle", "map", "statistics"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::01_Math_Foundations",
        "scenario": "ML Math: Hessian Matrix & Local Curvature 📈",
        "text": "In multi-variable optimization, the {{c1::Hessian matrix}} is a square matrix of second-order partial derivatives that describes the local curvature of a function, allowing us to determine if a critical point is a local minimum when the matrix is {{c2::positive definite}}.",
        "explanation": "If the Hessian matrix H is positive definite (H > 0), the function curves upwards in all directions, representing a local minimum. In optimization, Newton's method uses the inverse Hessian to scale the gradient step, providing quadratic convergence.",
        "usage": "Used in advanced optimization algorithms (e.g., Newton-Raphson, BFGS, and XGBoost's split criterion).",
        "spanish": "En optimización multivariable, la matriz Hessiana es una matriz cuadrada de segundas derivadas parciales que describe la curvatura local de una función, lo que nos permite determinar si un punto crítico es un mínimo local cuando la matriz es definida positiva.",
        "tags": ["math", "hessian", "calculus"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::01_Math_Foundations",
        "scenario": "ML Math: The Curse of Dimensionality 🌌",
        "text": "As the number of features increases, the volume of the space grows exponentially, causing data points to become extremely sparse and the Euclidean distance between any two points to {{c1::converge to a constant value}}.",
        "explanation": "In high-dimensional spaces, the difference between the distance to the nearest point and the distance to the farthest point approaches zero relative to the distance itself. This renders distance-based algorithms (like KNN and K-Means) highly ineffective without dimensionality reduction.",
        "usage": "Explains why high-dimensional features require regularization or PCA/UMAP pre-processing.",
        "spanish": "A medida que aumenta el número de características, el volumen del espacio crece exponencialmente, lo que hace que los puntos de datos se vuelvan extremadamente dispersos y que la distancia euclidiana entre dos puntos cualesquiera converja a un valor constante.",
        "tags": ["math", "curse_of_dimensionality", "distance"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::01_Math_Foundations",
        "scenario": "ML Math: Bootstrapping Sampling Mechanics 🎲",
        "text": "The statistical technique of {{c1::Bootstrapping}} estimates the sampling distribution of an estimator by performing {{c2::random sampling with replacement}} from the original dataset.",
        "explanation": "Bootstrapping generates multiple 'new' datasets of the same size as the original by drawing samples repeatedly, allowing some items to be selected multiple times (about 63.2% of original unique points are selected per bootstrap sample on average). It is used to calculate confidence intervals and stability.",
        "usage": "The core sampling mechanism behind bagging algorithms like Random Forest (where out-of-bag samples act as validation).",
        "spanish": "La técnica estadística de Bootstrapping estima la distribución muestral de un estimador al realizar un muestreo aleatorio con reemplazo del conjunto de datos original.",
        "tags": ["math", "bootstrapping", "sampling"]
    },

    # 02_Feature_Engineering
    {
        "deck": "AI_Learning_Path::01_Classical_ML::02_Feature_Engineering",
        "scenario": "Preprocessing: MICE Missing Data Imputation 🧬",
        "text": "For handling missing data, Multivariate Imputation by Chained Equations (MICE) imputes variables by modeling each variable with missing values as a function of {{c1::all other variables}} in an {{c2::iterative, series-of-regressions loop}}.",
        "explanation": "Unlike simple mean/median imputation, MICE preserves the multivariate relationship between features. It runs multiple regression passes (chained equations), drawing values from the predictive distributions to create multiple complete datasets.",
        "usage": "Standard for clinical trials and datasets where missing values are not missing completely at random (MAR/MNAR).",
        "spanish": "Para el manejo de datos faltantes, la Imputación Multivariable por Ecuaciones Encadenadas (MICE) imputa variables modelando cada variable con valores faltantes en función de todas las demás variables en un ciclo iterativo de regresiones.",
        "tags": ["preprocessing", "mice", "imputation"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::02_Feature_Engineering",
        "scenario": "Preprocessing: Target Encoding & Data Leakage 🧯",
        "text": "To prevent data leakage during Target Encoding of high-cardinality categorical features, developers apply {{c1::K-Fold target encoding}} or add {{c2::smoothing/additive noise}} based on global prior distributions.",
        "explanation": "Target encoding replaces categories with the mean target value. If computed directly on the whole dataset, it leaks the label into the feature, causing extreme overfitting. K-Fold target encoding calculates the category means using only out-of-fold data points.",
        "usage": "Critical for high-cardinality variables (e.g. ZIP codes, device IDs) in gradient boosted tree models.",
        "spanish": "Para evitar la filtración de datos durante la codificación de objetivo de características categóricas de alta cardinalidad, los desarrolladores aplican codificación de objetivo K-Fold o añaden suavizado/ruido aditivo basado en distribuciones globales a priori.",
        "tags": ["preprocessing", "target_encoding", "data_leakage"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::02_Feature_Engineering",
        "scenario": "Preprocessing: Box-Cox vs Yeo-Johnson Transformations 📈",
        "text": "While the Box-Cox transformation requires the input feature to be {{c1::strictly positive}}, the Yeo-Johnson transformation extends this capability to support {{c2::zero and negative values}}.",
        "explanation": "Both methods find a power parameter lambda using maximum likelihood to stabilize variance and make data closely conform to a normal distribution. Yeo-Johnson uses modified formulas to handle negative numbers, making it more robust in general preprocessing.",
        "usage": "Applied to highly skewed features before training linear regression or neural network models.",
        "spanish": "Mientras que la transformación Box-Cox requiere que la característica de entrada sea estrictamente positiva, la transformación Yeo-Johnson extiende esta capacidad para admitir valores cero y negativos.",
        "tags": ["preprocessing", "transformations", "normalization"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::02_Feature_Engineering",
        "scenario": "Preprocessing: Recursive Feature Elimination (RFE) ✂️",
        "text": "Recursive Feature Elimination (RFE) is a wrapper method that selects features by training an estimator, ranking features by their weights/importances, and {{c1::iteratively removing the least important features}} until the target subset size is reached.",
        "explanation": "RFE accounts for feature dependencies by retraining the model after each removal step. While computationally expensive, it provides a much more accurate feature subset than simple filter methods that evaluate features independently.",
        "usage": "Commonly combined with SVMs or Random Forests to optimize input dimensions.",
        "spanish": "La Eliminación Recursiva de Características (RFE) es un método de envoltura que selecciona características entrenando un estimador, clasificando características por sus pesos e iterativamente eliminando las menos importantes hasta alcanzar el tamaño de subconjunto deseado.",
        "tags": ["preprocessing", "rfe", "feature_selection"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::02_Feature_Engineering",
        "scenario": "Preprocessing: t-SNE vs UMAP Manifold Learning 🌐",
        "text": "While t-SNE focuses on preserving {{c1::local pairwise distances (neighborhoods)}} using probability distributions, UMAP preserves both local and {{c2::global structural relationships}} using Riemannian geometry.",
        "explanation": "t-SNE maps similarities in low dimensions using a Student-t distribution, which tends to crowd clusters and lose global spacing. UMAP assumes data lies on a manifold and preserves its topology, resulting in much faster computation and better representation of global structures.",
        "usage": "Used to visualize high-dimensional embeddings and cluster outputs in 2D or 3D.",
        "spanish": "Mientras que t-SNE se centra en preservar las distancias locales por pares utilizando distribuciones de probabilidad, UMAP preserva tanto las relaciones estructurales locales como globales utilizando geometría de Riemann.",
        "tags": ["preprocessing", "tsne", "umap", "dimensionality_reduction"]
    },

    # 03_Supervised_Algorithms
    {
        "deck": "AI_Learning_Path::01_Classical_ML::03_Supervised_Algorithms",
        "scenario": "Supervised: ElasticNet Regularization ⚖️",
        "text": "The ElasticNet loss function combines L1 (Lasso) and L2 (Ridge) penalties by minimizing the objective function with two hyperparameters: {{c1::alpha (overall penalty multiplier)}} and {{c2::l1_ratio (balance between L1 and L2 terms)}}.",
        "explanation": "Lasso (L1) forces weights to absolute zero (sparse models), but struggles with highly correlated features (it randomly selects one). Ridge (L2) shrinks weights together. ElasticNet balances both, allowing group selection of correlated features while maintaining sparsity.",
        "usage": "Standard regularized linear model when features are highly collinear and high-dimensional.",
        "spanish": "La función de pérdida de ElasticNet combina las penalizaciones L1 (Lasso) y L2 (Ridge) al minimizar la función objetivo con dos hiperparámetros: alfa y l1_ratio.",
        "tags": ["supervised", "elasticnet", "regularization"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::03_Supervised_Algorithms",
        "scenario": "Supervised: SVM Kernel Trick & Mercer's Theorem 🛡️",
        "text": "The SVM Kernel Trick computes dot products in a high-dimensional feature space without explicitly mapping data points, provided the kernel function satisfies {{c1::Mercer's theorem (positive semi-definite kernel)}}.",
        "explanation": "Mapping data explicitly into infinite dimensions (like the RBF kernel does) is computationally impossible. By replacing the dot product Phi(x) . Phi(z) with a kernel function K(x, z), SVMs perform non-linear classification with high computational efficiency.",
        "usage": "Foundation of Support Vector Machines utilizing RBF, Polynomial, or Sigmoid kernels.",
        "spanish": "El truco del kernel de SVM calcula productos de puntos en un espacio de características de alta dimensión sin mapear explícitamente los puntos de datos, siempre que la función del kernel cumpla con el teorema de Mercer.",
        "tags": ["supervised", "svm", "kernel_trick"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::03_Supervised_Algorithms",
        "scenario": "Supervised: XGBoost System Optimizations 🚀",
        "text": "XGBoost optimizes gradient boosting performance through system-level designs, including {{c1::block structure for parallel learning}}, {{c2::sparsity-aware split finding}} for missing values, and cache-aware access.",
        "explanation": "XGBoost stores sorted features in out-of-core blocks to parallelize tree splits. Its sparsity-aware algorithm assigns a default direction for missing values at each node based on which direction minimizes the gradient loss, greatly speeding up training.",
        "usage": "Critical for high-speed training of gradient boosted trees on massive tabular datasets.",
        "spanish": "XGBoost optimiza el rendimiento del aumento de gradiente a través de diseños a nivel de sistema, incluyendo estructura de bloques para aprendizaje paralelo y búsqueda de divisiones consciente de la dispersión para valores faltantes.",
        "tags": ["supervised", "xgboost", "boosting"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::03_Supervised_Algorithms",
        "scenario": "Supervised: LightGBM Leaf-Wise Growth 🌳",
        "text": "Unlike traditional depth-wise tree builders, LightGBM uses {{c1::leaf-wise (best-first) tree growth}}, which splits the leaf node that yields the {{c2::maximum loss reduction}} regardless of depth.",
        "explanation": "Depth-wise algorithms build trees level by level, splitting all nodes. Leaf-wise growth is more efficient, focusing only on high-error nodes. While leaf-wise growth can achieve much lower loss, it requires strict regularization (like limiting max_depth) to prevent overfitting.",
        "usage": "Applied in LightGBM to speed up convergence and handle large datasets with deep trees.",
        "spanish": "A diferencia de los constructores de árboles tradicionales por profundidad, LightGBM utiliza el crecimiento de árboles por hojas (el mejor primero), que divide el nodo hoja que produce la máxima reducción de pérdida.",
        "tags": ["supervised", "lightgbm", "tree_growth"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::03_Supervised_Algorithms",
        "scenario": "Supervised: CatBoost Categorical Splits 📊",
        "text": "CatBoost handles categorical features natively by calculating {{c1::ordered target statistics (ordered TS)}} on random permutations of the dataset, avoiding target leakage and overfitting.",
        "explanation": "Standard target statistics use future data within the target calculation, introducing bias. CatBoost permutes the dataset and, for each row, computes the target statistics using only the history of preceding rows in the permutation.",
        "usage": "Deployed for training models on tabular datasets containing rich categorical and text variables.",
        "spanish": "CatBoost maneja variables categóricas de forma nativa calculando estadísticas de objetivo ordenadas sobre permutaciones aleatorias del conjunto de datos, evitando la filtración de objetivo y el sobreajuste.",
        "tags": ["supervised", "catboost", "categorical"]
    },

    # 04_Unsupervised_Algorithms
    {
        "deck": "AI_Learning_Path::01_Classical_ML::04_Unsupervised_Algorithms",
        "scenario": "Unsupervised: DBSCAN Density Clustering 🛑",
        "text": "DBSCAN classifies points into core, border, and noise categories based on two parameters: {{c1::eps (epsilon neighborhood radius)}} and {{c2::minSamples (minimum points in radius)}}.",
        "explanation": "Core points have at least minSamples within their eps radius. Border points have fewer but are reachable from a core point. Noise points are unreachable. DBSCAN requires no predefined cluster count and can isolate complex, arbitrary cluster shapes.",
        "usage": "Excellent for spatial data, geospatial mapping, and anomaly detection.",
        "spanish": "DBSCAN clasifica los puntos en las categorías de núcleo, borde y ruido en función de dos parámetros: eps y minSamples.",
        "tags": ["unsupervised", "dbscan", "clustering"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::04_Unsupervised_Algorithms",
        "scenario": "Unsupervised: Silhouette Coefficient 📏",
        "text": "The Silhouette Coefficient measures clustering quality by comparing the mean intra-cluster distance a with the mean nearest-cluster distance b, using the formula {{c1::(b - a) / max(a, b)}}.",
        "explanation": "The coefficient ranges from -1 (poor clustering, points assigned to wrong clusters) to +1 (dense, well-separated clusters). A value near 0 indicates overlapping clusters. Plotting silhouette widths helps select the optimal number of clusters k.",
        "usage": "Evaluates K-Means or Hierarchical clustering stability.",
        "spanish": "El coeficiente de silueta mide la calidad del agrupamiento al comparar la distancia media intra-cluster a con la distancia media al cluster más cercano b, utilizando la fórmula (b - a) / max(a, b).",
        "tags": ["unsupervised", "silhouette", "clustering"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::04_Unsupervised_Algorithms",
        "scenario": "Unsupervised: GMM & Expectation-Maximization 🤝",
        "text": "Gaussian Mixture Models (GMM) perform soft-clustering by modeling data as a mixture of multiple normal distributions, optimizing parameters iteratively using the {{c1::Expectation-Maximization (EM) algorithm}}.",
        "explanation": "EM alternates between calculating the probability that each point belongs to each Gaussian cluster (Expectation step) and updating the means, covariances, and mixing coefficients of the Gaussians (Maximization step) until convergence.",
        "usage": "Used for probabilistic clustering and density estimation where data points have mixed cluster membership.",
        "spanish": "Los Modelos de Mezcla Gaussiana (GMM) realizan un agrupamiento suave al modelar los datos como una mezcla de múltiples distribuciones normales, optimizando los parámetros con el algoritmo Esperanza-Maximización (EM).",
        "tags": ["unsupervised", "gmm", "expectation_maximization"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::04_Unsupervised_Algorithms",
        "scenario": "Unsupervised: Isolation Forest Anomalies 🌲",
        "text": "Isolation Forest isolates anomalies by recursively partitioning features using random splits; anomalies are identified by their {{c1::short path lengths}} in the resulting isolation trees.",
        "explanation": "Because anomalies have unusual feature values, they require very few random splits to isolate them from the rest of the dataset. Therefore, anomaly points end up close to the root of the tree, resulting in short average path lengths across the forest.",
        "usage": "High-performance anomaly and fraud detection on tabular data.",
        "spanish": "Isolation Forest aísla anomalías al particionar recursivamente las características utilizando divisiones aleatorias; las anomalías se identifican por sus longitudes de ruta cortas en los árboles de aislamiento.",
        "tags": ["unsupervised", "isolation_forest", "anomaly_detection"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::04_Unsupervised_Algorithms",
        "scenario": "Unsupervised: Latent Dirichlet Allocation (LDA) 📚",
        "text": "Latent Dirichlet Allocation (LDA) models documents as mixtures of latent topics, assuming that topics follow a {{c1::Dirichlet prior distribution}} over words, and documents follow a {{c2::Dirichlet prior distribution}} over topics.",
        "explanation": "LDA is a generative probabilistic model. It models the generation of words in documents by drawing a topic from a document-topic distribution, and then drawing a word from the corresponding topic-word distribution, solved using Gibbs sampling.",
        "usage": "Topic extraction and document categorization in Natural Language Processing.",
        "spanish": "La Asignación Latente de Dirichlet (LDA) modela documentos como mezclas de temas latentes, asumiendo que los temas siguen una distribución a priori de Dirichlet sobre las palabras, y los documentos siguen una distribución a priori de Dirichlet sobre los temas.",
        "tags": ["unsupervised", "lda", "topic_modeling"]
    },

    # 05_Evaluation_Metrics
    {
        "deck": "AI_Learning_Path::01_Classical_ML::05_Evaluation_Metrics",
        "scenario": "Metrics: Matthews Correlation Coefficient (MCC) 📊",
        "text": "For highly imbalanced classification tasks, the {{c1::Matthews Correlation Coefficient (MCC)}} provides a more balanced metric than F1-score because it incorporates {{c2::all four quadrants of the confusion matrix}} (TP, TN, FP, FN).",
        "explanation": "F1-score ignores True Negatives (TN) entirely, which can lead to overoptimistic scores in imbalanced sets. MCC ranges from -1 (total disagreement) to +1 (perfect prediction) and only scores high if the model predicts well in all classes.",
        "usage": "Recommended metric for medical diagnostics and fraud detection evaluation.",
        "spanish": "Para tareas de clasificación altamente desbalanceadas, el Coeficiente de Correlación de Matthews (MCC) proporciona una métrica más equilibrada que la puntuación F1 porque incorpora los cuatro cuadrantes de la matriz de confusión.",
        "tags": ["evaluation", "mcc", "metrics"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::05_Evaluation_Metrics",
        "scenario": "Metrics: ROC-AUC vs PR-AUC 📈",
        "text": "While the ROC-AUC score is insensitive to class distribution changes, the Precision-Recall AUC (PR-AUC) is highly sensitive and preferred when evaluating {{c1::highly imbalanced datasets}} where the {{c2::positive class is rare}}.",
        "explanation": "ROC plots True Positive Rate against False Positive Rate. In highly imbalanced datasets, a large number of True Negatives keeps the False Positive Rate low, hiding classification errors. PR-AUC focuses on Precision and Recall, exposing false positives directly.",
        "usage": "Evaluating credit card fraud models or rare disease classification models.",
        "spanish": "Mientras que la puntuación ROC-AUC es insensible a los cambios en la distribución de clases, el AUC de Precisión-Recall (PR-AUC) es altamente sensible y se prefiere al evaluar conjuntos de datos muy desbalanceados.",
        "tags": ["evaluation", "auc", "metrics"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::05_Evaluation_Metrics",
        "scenario": "Metrics: Time Series Data Leakage ⏳",
        "text": "When validating time series models, standard K-Fold cross-validation causes data leakage by using {{c1::future data to predict past data}}; to prevent this, developers must use {{c2::Time Series Split (rolling window)}} validation.",
        "explanation": "Time series data is ordered. Predicting past values using future values violates temporal causality and overestimates model accuracy. Time Series Split ensures the training set only contains data that occurred prior to the validation set.",
        "usage": "Essential validation strategy for financial market forecasts and demand planning.",
        "spanish": "Al validar modelos de series temporales, la validación cruzada K-Fold estándar causa filtración de datos al usar datos futuros para predecir datos pasados; para evitar esto, los desarrolladores deben usar Time Series Split.",
        "tags": ["evaluation", "time_series", "data_leakage"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::05_Evaluation_Metrics",
        "scenario": "Metrics: Bias-Variance Decomposition 🔀",
        "text": "The expected prediction error of a model can be decomposed into three mathematical components: {{c1::squared bias (underfitting)}}, {{c2::variance (overfitting)}}, and {{c3::irreducible error (noise)}}.",
        "explanation": "Bias measures how much the average model prediction differs from the true value. Variance measures how much the predictions fluctuate across different training samples. Irreducible error is the inherent noise in the data generating process.",
        "usage": "Used to diagnose model training errors and decide between simple models or complex models.",
        "spanish": "El error de predicción esperado de un modelo puede descomponerse en tres componentes matemáticos: sesgo al cuadrado (subajuste), varianza (sobreajuste) y error irreducible (ruido).",
        "tags": ["evaluation", "bias_variance", "diagnostics"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::05_Evaluation_Metrics",
        "scenario": "Metrics: F-Beta Score Calibration 🎯",
        "text": "The F-Beta Score generalizes the F1-score by introducing a coefficient beta that weights the relative importance of precision and recall: setting beta = 2 weights {{c1::recall higher than precision}}, while beta = 0.5 weights {{c2::precision higher than recall}}.",
        "explanation": "The formula balances precision and recall. A beta of 2 is used when false negatives are extremely costly (e.g. failing to detect cancer). A beta of 0.5 is used when false positives are extremely costly (e.g. blocking a customer's credit card).",
        "usage": "Fine-tuning classifier metrics to match specific business costs.",
        "spanish": "La puntuación F-Beta generaliza la puntuación F1 al introducir un coeficiente beta que pondera la importancia relativa de precisión y recall: configurar beta = 2 pondera recall más alto que precisión.",
        "tags": ["evaluation", "f_beta", "metrics"]
    },

    # 06_Optimization_Explicability
    {
        "deck": "AI_Learning_Path::01_Classical_ML::06_Optimization_Explicability",
        "scenario": "Explainability: Bayesian Optimization acquisition 📐",
        "text": "In hyperparameter tuning, Bayesian Optimization uses a Gaussian Process surrogate model and an {{c1::Acquisition Function (e.g., Expected Improvement)}} to balance {{c2::exploration of unknown spaces}} with {{c3::exploitation of known optimal regions}}.",
        "explanation": "Instead of searching parameters randomly, Bayesian Optimization models the objective function probabilistically. The acquisition function calculates the utility of evaluating a set of hyperparameters next, maximizing the probability of finding a better model.",
        "usage": "Hyperparameter tuning utilizing packages like Optuna, Hyperopt, or Scikit-Optimize.",
        "spanish": "En el ajuste de hiperparámetros, la optimización bayesiana utiliza un modelo sustituto de proceso gaussiano y una función de adquisición para equilibrar la exploración con la explotación.",
        "tags": ["optimization", "bayesian_optimization", "optuna"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::06_Optimization_Explicability",
        "scenario": "Explainability: Probability Calibration Platt Scaling ⚖️",
        "text": "To calibrate classification model outputs into true probabilities, {{c1::Platt Scaling}} fits a {{c2::logistic regression model}} on the raw decision scores generated by algorithms like SVM or Naive Bayes.",
        "explanation": "Models like SVM yield raw distance metrics, not probabilities. Naive Bayes outputs extreme, uncalibrated probabilities near 0 or 1 due to the independence assumption. Platt Scaling maps these scores to calibrated probability outputs using a logistic sigmoid.",
        "usage": "Calibration of model confidence scores for risk analysis and decision systems.",
        "spanish": "Para calibrar las salidas del modelo de clasificación en probabilidades reales, Platt Scaling ajusta un modelo de regresión logística en las puntuaciones de decisión brutas generadas por algoritmos como SVM.",
        "tags": ["optimization", "calibration", "platt_scaling"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::06_Optimization_Explicability",
        "scenario": "Explainability: SHAP Shapley Additive Explanations 🔍",
        "text": "SHAP calculates feature importance by using cooperative game theory to distribute the model output payoff among features, ensuring mathematical consistency through the {{c1::Additivity and Efficiency axioms}}.",
        "explanation": "SHAP values compute the marginal contribution of each feature across all possible feature subsets (coalitions). Unlike heuristic importance methods, SHAP guarantees consistency: if a model changes so that a feature has more impact, its SHAP value cannot decrease.",
        "usage": "Industry standard for local and global model explainability in regulated domains.",
        "spanish": "SHAP calcula la importancia de las características utilizando la teoría de juegos cooperativos para distribuir el rendimiento del modelo entre las características, garantizando la consistencia matemática.",
        "tags": ["optimization", "explainability", "shap"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::06_Optimization_Explicability",
        "scenario": "Explainability: LIME Local Interpretability 🎯",
        "text": "LIME explains individual predictions by perturbing the input sample, generating local predictions, and fitting a {{c1::simple, interpretable surrogate model (e.g., linear regression)}} weighted by proximity.",
        "explanation": "LIME assumes that while a complex model (e.g., random forest or neural network) is globally non-linear, it can be approximated locally around a specific data point using a simple linear model.",
        "usage": "Local interpretability for black-box models on tabular, text, or image data.",
        "spanish": "LIME explica las predicciones individuales al perturbar la muestra de entrada, generar predicciones locales y ajustar un modelo sustituto simple e interpretable ponderado por la proximidad.",
        "tags": ["optimization", "explainability", "lime"]
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML::06_Optimization_Explicability",
        "scenario": "Explainability: Data Drift vs Concept Drift ⏱️",
        "text": "While Data Drift represents a change in the {{c1::input feature distribution P(X)}}, Concept Drift represents a change in the {{c2::relationship between features and the target label P(Y|X)}}.",
        "explanation": "Data Drift occurs when the user demographic shifts (e.g. younger users join the app). Concept Drift occurs when external realities change, rendering the model's logic obsolete (e.g. a change in macroeconomic policies makes past credit score behaviors invalid).",
        "usage": "Monitoring model decay, pipeline degradation, and planning retraining schedules in production.",
        "spanish": "Mientras que la deriva de datos representa un cambio en la distribución de características de entrada P(X), la deriva de concepto representa un cambio en la relación entre las características y la etiqueta objetivo P(Y|X).",
        "tags": ["optimization", "drift", "monitoring"]
    }
]

# Avoid adding duplicates
existing_scenarios = {c["scenario"] for c in cards}
added_count = 0

for card in new_cards:
    if card["scenario"] not in existing_scenarios:
        cards.append(card)
        added_count += 1

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added_count} new cards. Total cards in database: {len(cards)}.")
