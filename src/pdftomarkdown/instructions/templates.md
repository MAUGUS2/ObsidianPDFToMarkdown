# {{ title }}
{{ lesson_description }}

---

## Temas 
{% for tema in temas %}
## {{ tema.name }}
{{ tema.description }}

  - **Tópicos:**
  {% for topico in tema.topics %}
  - **{{ topico.name }}**: {{ topico.description }}
  {% endfor %}

  {{ tema.content }}
  { Use the Obsidian formatting tools that best fit this theme to enhance visual content. }

  {% for topico in tema.topics %}
  ### {{ topico.name }}
  {{ topico.description }}

    - **Subtópicos:**
    {% for subtopico in topico.subtopics %}
    - **{{ subtopico.name }}**: {{ subtopico.description }}
    {% endfor %}

    {{ topico.content }}
    { Use the Obsidian formatting tools that best fit this topic to enhance visual content. }

    {% for subtopico in topico.subtopics %}
    #### {{ subtopico.name }}
    {{ subtopico.description }}

    {{ subtopico.content }}
    { Use the Obsidian formatting tools that best fit this subtopic to enhance visual content. }

    {% if subtopico.subsubtopics %}
    **Sub-subtópicos:**
    {% for subsubtopico in subtopico.subsubtopics %}
    - **{{ subsubtopico.name }}**: {{ subsubtopico.description }}
    {% endfor %}
    
    {% for subsubtopico in subtopico.subsubtopics %}
    ##### {{ subsubtopico.name }}
    {{ subsubtopico.description }}

    {{ subsubtopico.content }}

    **Exemplos Práticos:**
    {{ subsubtopico.practical_examples }}

    > [!tip] **Dica:**
    > {{ subsubtopico.tip }}

    > [!info] **Nota:**
    {{ subsubtopico.notice | default('Nenhuma nota adicional') }}

    **Técnicas de Estudo Aplicadas:**
    - **Aprendizagem ativa:** {{ subsubtopico.techniques.active_learning | default('Não aplicado') }}
    - **Repetição espaçada:** {{ subsubtopico.techniques.spaced_repetition | default('Não aplicado') }}
    - **Prática intercalada:** {{ subsubtopico.techniques.interleaved_practice | default('Não aplicado') }}
    - **Auto-teste:** {{ subsubtopico.techniques.self_testing | default('Não aplicado') }}
    - **Mapeamento de conceitos:** {{ subsubtopico.techniques.concept_mapping | default('Não aplicado') }}
    - **Codificação dual:** {{ subsubtopico.techniques.dual_coding | default('Não aplicado') }}
    - **Elaboração:** {{ subsubtopico.techniques.elaboration | default('Não aplicado') }}
    - **Gestão de distrações:** {{ subsubtopico.techniques.distraction_management | default('Não aplicado') }}
    - **Revisão de erros:** {{ subsubtopico.techniques.error_review | default('Não aplicado') }}
    - **Trabalho profundo:** {{ subsubtopico.techniques.deep_work | default('Não aplicado') }}

    {% endfor %}
    {% endif %}

    **Exemplos Práticos:**
    {{ subtopico.practical_examples }}

    > [!tip] **Dica:**
    > {{ subtopico.tip }}

    > [!info] **Nota:**
    {{ subtopico.notice | default('Nenhuma nota adicional') }}

    **Técnicas de Estudo Aplicadas:**
    - **Aprendizagem ativa:** {{ subtopico.techniques.active_learning | default('Não aplicado') }}
    - **Repetição espaçada:** {{ subtopico.techniques.spaced_repetition | default('Não aplicado') }}
    - **Prática intercalada:** {{ subtopico.techniques.interleaved_practice | default('Não aplicado') }}
    - **Auto-teste:** {{ subtopico.techniques.self_testing | default('Não aplicado') }}
    - **Mapeamento de conceitos:** {{ subtopico.techniques.concept_mapping | default('Não aplicado') }}
    - **Codificação dual:** {{ subtopico.techniques.dual_coding | default('Não aplicado') }}
    - **Elaboração:** {{ subtopico.techniques.elaboration | default('Não aplicado') }}
    - **Gestão de distrações:** {{ subtopico.techniques.distraction_management | default('Não aplicado') }}
    - **Revisão de erros:** {{ subtopico.techniques.error_review | default('Não aplicado') }}
    - **Trabalho profundo:** {{ subtopico.techniques.deep_work | default('Não aplicado') }}

    {% endfor %}

  {% endfor %}

{% endfor %}

---

## Conclusão da Aula
{{ lesson_conclusion }}

---

## Referências e Leituras Recomendadas
{{ references_and_readings }}
