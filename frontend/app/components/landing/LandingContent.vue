<template>
    <div class="content">
        <LandingSection id="background" title="背景：サーバーの仮想化とオーケストレーション"
            lead="近年のサーバーセンターでは、コンピューター内で動かすプログラムをコンテナ(Pod)化し、マシン(Node)間で柔軟に配置・移動させることで、資源の有効活用と運用の自動化を図っています。コンテナをどこのサーバーに置くかを決める仕組みをオーケストレーションといい、Kubernetesなどが有名です。">
            <div class="grid">
                <div class="card">
                    <h3 class="card-title">複数マシンの協調管理</h3>
                    <p class="para">
                        たくさんのサーバーをまとめて一つの大きなコンピューターのように扱い、
                        コンテナを効率よく配置・移動させることで、資源の無駄を減らします。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">障害時の冗長性</h3>
                    <p class="para">
                        どこかのサーバーが故障しても、すぐに別のマシンにコンテナを移してサービスを継続します。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">負荷変動への対応</h3>
                    <p class="para">
                        負荷が高いサーバーから低いサーバーへコンテナを移動させることで、
                        全体の負荷を均等に保ち、性能低下を防ぎます。
                    </p>
                </div>
            </div>
        </LandingSection>

        <LandingSection id="challenges" title="課題点：多様な制約が絡み合う配置問題"
            lead="コンテナの配置問題では、複数の制約条件を同時に満たす必要があり、それらが互いに衝突することで最適化が困難になります。">

            <div class="grid">
                <div class="card">
                    <h3 class="card-title">容量制約</h3>
                    <p class="para">
                        各サーバーには <strong>CPU・メモリ・ストレージ</strong> などの物理的な上限があります。
                        この容量を超えてコンテナを配置することはできません。
                    </p>
                    <ul class="list">
                        <li>CPU使用率の上限</li>
                        <li>メモリ容量の上限</li>
                        <li>ストレージ・帯域の制限</li>
                    </ul>
                </div>
                <div class="card">
                    <h3 class="card-title">配置ルール制約</h3>
                    <p class="para">
                        運用上の理由から、コンテナの配置場所に <strong>ルール</strong> が設けられることがあります。
                    </p>
                    <ul class="list">
                        <li>同一サービスは別サーバーに分散（冗長性）</li>
                        <li>特定のサーバーへの配置禁止（メンテ中など）</li>
                        <li>GPU等の特殊ハードウェア要件</li>
                    </ul>
                </div>
                <div class="card">
                    <h3 class="card-title">移動コスト制約</h3>
                    <p class="para">
                        コンテナの移動には <strong>コスト</strong> が伴います。無制限に移動させると運用に悪影響が出ます。
                    </p>
                    <ul class="list">
                        <li>移動中のサービス一時停止・遅延</li>
                        <li>ネットワーク・ディスクI/Oの増加</li>
                        <li>監視・復旧の運用負担</li>
                    </ul>
                </div>
            </div>

            <div class="note">
                <div class="note-title">制約の衝突が問題を難しくする</div>
                <div class="note-text">
                    これらの制約は互いに衝突します。例えば「負荷を均等にしたい」と「移動を減らしたい」は相反し、
                    「冗長性を高めたい」と「資源効率を上げたい」もトレードオフの関係にあります。
                    単純なルールベースの手法ではすべてを満たすことが難しく、多目的最適化が必要になります。
                </div>
            </div>
        </LandingSection>

        <LandingSection id="solution" title="解決策：量子アニーリングで“多目的最適化”を一撃で"
            lead="置き場所の組合せ（0/1）を一つの最適化問題にまとめ、アニーリングで“良い配置”を探します。負荷の偏りと移動量を同時に小さくします。">
            <div class="two-col">
                <div class="card">
                    <h3 class="card-title">入力（観測）</h3>
                    <ul class="list">
                        <li>サーバーのスペック（CPU/メモリ）</li>
                        <li>コンテナごとの必要量（CPU/メモリ、優先度）</li>
                        <li>現在のコンテナ配置</li>
                        <li>移動コスト（影響が大きいものほど高い）</li>
                        <li>アンチアフィニティ（同一サービス分散）</li>
                    </ul>
                </div>

                <div class="card">
                    <h3 class="card-title">出力（意思決定）</h3>
                    <ul class="list">
                        <li>変更後のコンテナ配置</li>
                    </ul>
                </div>
            </div>

            <div class="cards-3">
                <div class="card emphasis">
                    <div class="badge">Key</div>
                    <h3 class="card-title">最小の移動</h3>
                    <p class="para">
                        メモリやCPUの使用率が高いコンテナほど移動コストを高く設定することで、負荷が跳ね上がったタスクがあるときはそれ以外のコンテナをどかすよう促します。
                    </p>
                </div>
                <div class="card emphasis">
                    <div class="badge">Key</div>
                    <h3 class="card-title">均等な負荷</h3>
                    <p class="para">
                        各サーバーの理想負荷からのズレを二乗で評価し、マシンの劣化を均等にします。マシン間の性能差も適切に考慮します。
                    </p>
                </div>
                <div class="card emphasis">
                    <div class="badge">Key</div>
                    <h3 class="card-title">分散配置</h3>
                    <p class="para">
                        同一サービスの同居をペナルティ化して、冗長性とスパイク耐性を高めます。これによりマシン障害時にサービスを維持しやすくなります。
                    </p>
                </div>
                <div class="card emphasis">
                    <div class="badge">Key</div>
                    <h3 class="card-title">新規追加ノードの自動配置</h3>
                    <p class="para">
                        新しいサーバーが追加された場合、負荷を計算して適切なノードを活用するよう促します。
                    </p>
                </div>
                <div class="card emphasis">
                    <div class="badge">Key</div>
                    <h3 class="card-title">障害/退役の自動退避</h3>
                    <p class="para">
                        ノード停止、隔離、メンテナンス時は停止したコンテナを新規配置ノードとして扱い、適切なノードに再配置します。
                    </p>
                </div>
            </div>
        </LandingSection>

        <ClientOnly>
            <LandingSection id="formulation" title="定式化とその解説（現状のモデル）"
                lead="割当を0/1の変数で表し、(1)負荷の偏り、(2)移動のコスト、(3)同じサービスの同居 を一つの目的関数にまとめています。">
                <div class="card">
                    <h3 class="card-title">目的関数（全体像）</h3>
                    <LandingKatexMath
                        tex="\min \quad E_{\text{load}} \cdot w_{\text{load}} + E_{\text{move}} \cdot w_{\text{move}} + E_{\text{anti}} \cdot w_{\text{anti}}"
                        :block="true" />
                    <p class="para">
                        システム全体のコスト（エネルギー）を最小化します。
                        <strong>負荷分散</strong>、<strong>移動コスト</strong>、<strong>アンチアフィニティ</strong>の3つの項を重み付けして合算し、総合的に最適な配置を導き出します。
                    </p>
                </div>

                <div class="two-col">
                    <div class="card emphasis">
                        <div class="badge">Term 1</div>
                        <h3 class="card-title">負荷分散項</h3>
                        <LandingKatexMath
                            tex="E_{\text{load}} = \sum_{n} \left[ \left( L_n^{\text{cpu}} - \bar{L}_n^{\text{cpu}} \right)^2 + \left( L_n^{\text{mem}} - \bar{L}_n^{\text{mem}} \right)^2 \right]"
                            :block="true" />
                        <p class="para">
                            各ノードの実際の負荷と「理想負荷」のズレを二乗和で評価します。
                            偏りが大きいほどペナルティが増え、均等な配置を促します。
                        </p>
                        <div class="formula-detail">
                            <LandingKatexMath tex="L_n^{\text{cpu}} = \sum_{p} x_{p,n} \cdot \text{cpuReq}_p"
                                :block="true" />
                            <div class="formula-desc">ノード <LandingKatexMath tex="n" /> に配置されたPodのCPU要求量の合計</div>
                            <LandingKatexMath
                                tex="\bar{L}_n^{\text{cpu}} = \frac{\sum_p \text{cpuReq}_p}{\sum_{n'} \text{cpuCap}_{n'}} \cdot \text{cpuCap}_n"
                                :block="true" />
                            <div class="formula-desc">ノード <LandingKatexMath tex="n" /> の容量に比例した「理想的なCPU負荷」</div>
                        </div>
                    </div>

                    <div class="card emphasis">
                        <div class="badge">Term 2</div>
                        <h3 class="card-title">移動コスト項</h3>
                        <LandingKatexMath tex="E_{\text{move}} = \sum_{p} \sum_{n} x_{p,n} \cdot \text{moveCost}_{p,n}"
                            :block="true" />
                        <p class="para">
                            Podを現在のノードから別のノードに移動させるコストを評価します。
                            移動が多いほどペナルティが増え、不要な再配置を抑制します。
                        </p>
                        <div class="formula-detail">
                            <div class="formula-desc">
                                <LandingKatexMath tex="\text{moveCost}" /> は以下で構成：
                            </div>
                            <ul class="list">
                                <li>基本移動コスト（1.0）</li>
                                <li>Podの優先度に応じた追加コスト</li>
                                <li>リソース使用量に比例したコスト</li>
                            </ul>
                            <div class="formula-desc">現在のノードに留まる場合、および新規コンテナの場合はコスト0です。</div>
                        </div>
                    </div>
                </div>

                <div class="card emphasis">
                    <div class="badge">Term 3</div>
                    <h3 class="card-title">アンチアフィニティ項</h3>
                    <LandingKatexMath
                        tex="E_{\text{anti}} = \sum_{n} \sum_{p} \sum_{p'} \text{antiAffinity}_{p,p'} \cdot x_{p,n} \cdot x_{p',n}"
                        :block="true" />
                    <p class="para">
                        同じサービスに属するPod同士が同じノードに配置されるとペナルティを与えます。
                        これにより、サービスの冗長性を高め、1台のノード障害時の影響を軽減します。
                    </p>
                    <div class="formula-detail">
                        <div class="formula-desc">
                            <LandingKatexMath tex="\text{antiAffinity}" /> 行列は、同じ <LandingKatexMath tex="\text{service}" /> を持つPodペアに対して1.0、それ以外は0.0を設定。
                            <LandingKatexMath tex="x_{p,n} \cdot x_{p',n} = 1" /> となるのは両方のPodが同じノードに配置された場合のみです。
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3 class="card-title">制約条件</h3>
                    <LandingKatexMath tex="\sum_{n} x_{p,n} = 1 \quad \forall p" :block="true" />
                    <p class="para">
                        <strong>One-hot制約</strong>：各Podは必ず1つのノードに割り当てられます。
                        これにより、「どこにも配置されない」「複数ノードに重複配置」を防ぎます。
                    </p>
                </div>

                <div class="card">
                    <h3 class="card-title">決定変数</h3>
                    <LandingKatexMath tex="x_{p,n} \in \{0, 1\}" :block="true" />
                    <p class="para">
                        Pod <LandingKatexMath tex="p" /> がノード <LandingKatexMath tex="n" /> に配置される場合は1、そうでない場合は0を取る二値変数です。
                        すべてのPod×ノードの組み合わせに対してこの変数が定義され、最適化によってその値が決定されます。
                    </p>
                </div>

                <div class="note">
                    <div class="note-title">重みパラメータによるチューニング</div>
                    <div class="note-text">
                        各項の重み（<LandingKatexMath tex="w_{\text{load}}, w_{\text{move}}, w_{\text{anti}}" />）を調整することで、
                        「負荷均等を優先」「移動を最小限に」「冗長性重視」など、運用方針に応じた最適化が可能です。
                    </div>
                </div>
            </LandingSection>
        </ClientOnly>

        <LandingSection id="future" title="今後やりたいこと" lead="オートスケーリングとQA接続を軸に、“オンライン最適化”としての価値を伸ばします。">
            <div class="grid">
                <div class="card">
                    <h3 class="card-title">オートスケーリング</h3>
                    <p class="para">
                        “再配置”だけでなく、コンテナ数の増減（作成/削除）まで意思決定に含めます。
                        需要に応じたスケールと配置を一体化します。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">QAとの直接接続</h3>
                    <p class="para">
                        量子アニーラ（QA）やハイブリッド実行環境へ直接投げ、
                        最新の状態に基づいて低レイテンシで高頻度の最適化を狙います。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">サーバー容量を考慮した自動停止</h3>
                    <p class="para">
                        CPU/メモリの使用率が限界に近づいた時、優先度の低いコンテナを自動的に停止し、全体の安定性を保ちます。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">運用制約の吸収</h3>
                    <p class="para">
                        物理的に別の場所へ分散、ハードウェア要件（GPU/特定機種など）、優先度、遅延目標などを段階的に統合。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">高速化と安定化</h3>
                    <p class="para">
                        前回の解を初期解にする、変更分だけ最適化する、重みを自動調整するなどで、より迅速で安定した最適化を目指します。
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">ネットワーク帯域の考慮</h3>
                    <p class="para">
                        コンテナ移動時のネットワーク負荷を考慮し、帯域制約を超えないように最適化します。
                    </p>
                </div>
            </div>
        </LandingSection>

        <div class="cta">
            <div class="cta-inner">
                <div class="cta-title">デモで挙動を見てみる</div>
                <div class="cta-text">
                    負荷が変動する中で、どれだけ「少ない移動」で均等化できるかを確認できます。
                </div>
                <NuxtLink class="cta-button" to="/demo">試す</NuxtLink>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
@use "sass:color";

.content {
    width: 100%;
}

.grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
}

.media {
    display: grid;
    grid-template-columns: 0.8fr 1.2fr;
    gap: 1rem;
    align-items: start;
}

.media-visual {
    border-radius: 16px;
    padding: 1rem;
    background: color.adjust($surface, $lightness: 0%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.caption {
    margin-top: 0.75rem;
    color: $on-surface;
    font-size: 0.9rem;
    line-height: 1.6;
}

.two-col {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}

.cards-3 {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
}

.card {
    border-radius: 16px;
    background: color.adjust($surface, $lightness: 0%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
    padding: 1.1rem 1.1rem;
    margin: 1rem 0;
}

.emphasis {
    background: color.adjust($primary, $alpha: -0.94);
}

.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 22px;
    padding: 0 0.55rem;
    border-radius: 999px;
    font-weight: 900;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    background: $primary;
    color: $on-primary;
    margin-bottom: 0.6rem;
}

.card-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: $on-surface-variant;
    margin-bottom: 0.65rem;
}

.para {
    color: $on-surface;
    line-height: 1.85;
    font-size: 0.98rem;
}

.list {
    margin: 0;
    padding-left: 1.1rem;
    color: $on-surface;
    line-height: 1.85;
}

.steps {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.9rem;
}

.step {
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
    border-radius: 16px;
    padding: 1rem;
    background: color.adjust($surface, $lightness: 0%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.step-badge {
    width: 34px;
    height: 34px;
    border-radius: 12px;
    background: color.adjust($primary, $alpha: -0.05);
    color: $on-primary;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
}

.step-title {
    font-weight: 900;
    color: $on-surface-variant;
}

.step-text {
    margin-top: 0.25rem;
    color: $on-surface;
    line-height: 1.6;
    font-size: 0.95rem;
}

.note {
    margin-top: 1.1rem;
    border-radius: 16px;
    padding: 1rem 1.1rem;
    background: color.adjust($secondary, $alpha: -0.92);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.highlights {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}

.highlight {
    border-radius: 16px;
    padding: 1rem 1.1rem;
    background: color.adjust($secondary, $alpha: -0.92);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.highlight-title {
    font-weight: 900;
    color: $on-surface-variant;
}

.highlight-text {
    margin-top: 0.4rem;
    color: $on-surface;
    line-height: 1.8;
}

.note-title {
    font-weight: 900;
    color: $on-surface-variant;
}

.note-text {
    margin-top: 0.35rem;
    color: $on-surface;
    line-height: 1.7;
}

.formula-detail {
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px dashed color.adjust($on-surface, $alpha: -0.8);
}

.formula-desc {
    margin-top: 0.4rem;
    margin-bottom: 0.8rem;
    color: $on-surface;
    font-size: 0.9rem;
    line-height: 1.6;
}

code {
    background: color.adjust($surface, $lightness: -2%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
    border-radius: 8px;
    padding: 0.15rem 0.35rem;
}

.code-card {
    margin-top: 1rem;
}

.code {
    margin: 0.75rem 0 0;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    background: color.adjust($surface, $lightness: -2%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
    overflow: auto;
    line-height: 1.6;
}

.timeline {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
}

.milestone {
    border-radius: 16px;
    padding: 1rem 1.1rem;
    background: color.adjust($surface, $lightness: 0%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.milestone-title {
    font-weight: 900;
    color: $on-surface-variant;
    margin-bottom: 0.35rem;
}

.milestone-text {
    color: $on-surface;
    line-height: 1.8;
}

.cta {
    width: 100%;
    padding: 2.5rem 1.25rem 3.5rem;
}

.cta-inner {
    max-width: 1100px;
    margin: 0 auto;
    border-radius: 18px;
    padding: 1.5rem 1.25rem;
    background: color.adjust($primary, $alpha: -0.92);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.cta-title {
    font-size: 1.25rem;
    font-weight: 900;
    color: $on-surface-variant;
}

.cta-text {
    margin-top: 0.4rem;
    color: $on-surface;
    line-height: 1.8;
}

.cta-button {
    margin-top: 0.9rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    background: $primary;
    color: $on-primary;
    font-weight: 800;
    transition: background-color 0.2s ease;

    &:hover {
        background: color.adjust($primary, $lightness: -10%);
    }
}

@media (max-width: 1000px) {
    .media {
        grid-template-columns: 1fr;
    }

    .grid {
        grid-template-columns: 1fr;
    }

    .two-col {
        grid-template-columns: 1fr;
    }

    .cards-3 {
        grid-template-columns: 1fr;
    }

    .steps {
        grid-template-columns: 1fr;
    }

    .timeline {
        grid-template-columns: 1fr;
    }

    .highlights {
        grid-template-columns: 1fr;
    }
}
</style>
