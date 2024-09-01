from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "ab",
            ["/æb/"],
            ["Abbreviation of <i>abdominal</i> <i>muscles</i>."],
            [
                "<i>(informal)</i> abdominal muscle. <small>[Mid 20<sup>th</sup> century.]</small>",
                "<i>(slang)</i> An abscess caused by injecting an illegal drug, usually heroin.",
                "<i>Abbreviation of</i> <b>abortion</b>.",
                "<i>(US)</i> The early stages of; the beginning process; the start.",
                "<i>(climbing, informal)</i> To abseil.",
                "<i>Abbreviation of</i> <b>abort</b>.",
                "<i>Abbreviation of</i> <b>about</b>.",
            ],
            [],
        ),
        (
            "cum",
            ["/kʊm/", "/kʌm/"],
            ["Learned borrowing from Latin <i>cum</i> (“with”)."],
            [
                "<i>Used in indicating a thing with two roles, functions, or natures, or a thing that has changed from one to another.</i>",  # noqa
                "<i>Used in indicating a thing with two or more roles, functions, or natures, or a thing that has changed from one to another.</i>",  # noqa
                "<i>(colloquial, vulgar)</i> Semen.",
                "<i>(colloquial, vulgar)</i> Female ejaculatory discharge.",
                "<i>(colloquial, vulgar)</i> An ejaculation.",
                "<i>(slang)</i> To have an orgasm, to feel the sensation of an orgasm.",
                "<i>(slang)</i> To ejaculate.",
                "<i>Eye dialect spelling of</i> <b>come</b> (“move from further to nearer; arrive”).",
                "<i>Clipping of</i> <b>cumulative</b>.",
            ],
            [],
        ),
        (
            "efficient",
            ["/əˈfɪʃənt/", "/ɪˈfɪʃənt/"],
            [
                "1398, “making,” from Old French, from Latin <i>efficientem</i>, nominative <i>efficiēns</i>, participle of <i>efficere</i> (“work out, accomplish”) (see <i>effect</i>). Meaning “productive, skilled” is from 1787. <i>Efficiency apartment</i> is first recorded 1930, American English."  # noqa
            ],
            [
                "making good, thorough, or careful use of resources; not consuming extra. Especially, making good use of time or energy",  # noqa
                "expressing the proportion of consumed energy that was successfully used in a process; the ratio of useful output to total input",  # noqa
                "causing effects, producing results; bringing into being; initiating change (rare except in philosophical and legal expression <i>efficient cause</i> = causative factor or agent)",  # noqa
                "<i>(proscribed, old use)</i> effective, efficacious",
                "<i>(obsolete)</i> a cause; something that causes an effect",
            ],
            [],
        ),
        ("humans", [], [], [], ["human"]),
        (
            "it's",
            ["/ɪts/"],
            ["Contraction of ‘it is’ or ‘it has’."],
            [
                "<i>Contraction of</i> <b>it is</b>.",
                "<i>Contraction of</i> <b>it has</b>.",
                "<i>(dialectal, African-American Vernacular)</i> There's, there is; there're, there are.",  # noqa
                "<i>Obsolete form of</i> <b>its</b>.",
                "<i>Misspelling of</i> <b>its</b>.",
            ],
            [],
        ),
        (
            "Mars",
            ["/ˈmɑɹz/", "/ˈmɑːz/"],
            [
                "From Middle English <i>Mars</i>, from Latin <i>Mārs</i> (“god of war”), from older Latin (older than 75 <small>B.C.E.</small>) <i>Māvors</i>. <i>𐌌𐌀𐌌𐌄𐌓𐌔</i> was his Oscan name. He was also known as <i>Marmor</i>, <i>Marmar</i> and <i>Maris</i>, the latter from the Etruscan deity Maris."  # noqa
            ],
            [
                "<i>(astronomy)</i> The fourth planet in the solar system. Symbol: <b>♂</b>",
                "<i>(Roman mythology)</i> The Roman god of war.",
                "<i>(poetic)</i> War; a personification of war.",
                "The Mars Bar, a brand of chocolate bar with caramel and nougat filling.",
                "<i>Alternative form of</i> <b>Mas</b>",
            ],
            [],
        ),
        ("memoized", [], [], [], ["memoize"]),
        (
            "portmanteau",
            ["/pɔːtˈmæn.təʊ/", "/pɔːɹtˈmæntoʊ/", "/ˌpɔːɹtmænˈtoʊ/"],
            [
                "Middle French <i>portemanteau</i> (“coat stand”), from <i>porte</i> (“carry”) + <i>manteau</i> (“coat”)."  # noqa
            ],
            [
                "A large travelling case usually made of leather, and opening into two equal sections.",
                "<i>(Australia, dated)</i> A schoolbag.",
                "<i>(archaic)</i> A hook on which to hang clothing.",
                "<i>(linguistics)</i> A portmanteau word.",
                "A portmanteau film.",
                "<i>(attributive, linguistics)</i> Made by combining two (or more) words, stories, etc., in the manner of a linguistic portmanteau.",  # noqa
                "To make a portmanteau word.",
            ],
            [],
        ),
        (
            "someone",
            ["/ˈsʌmwʌn/"],
            ["From <i>some</i>&nbsp;+&nbsp;<i>one</i>."],
            [
                "some person.",
                "A partially specified but unnamed person.",
                "an important person",
            ],
            [],
        ),
        (
            "the",
            ["/ði/", "/ðə/", "/ðɪ/", "/ˈðiː/", "/ˈðʌ/"],
            [
                "From Middle English <i>þe</i>, from Old English <i>þē</i> <i>m</i> (“the, that”, demonstrative pronoun), a late variant of <i>sē</i>, the <i>s-</i> (which occurred in the masculine and feminine nominative singular only) having been replaced by the <i>þ-</i> from the oblique stem.",  # noqa
                "Originally neutral nominative, in Middle English it superseded all previous Old English nominative forms (<i>sē</i> <i>m</i>, <i>sēo</i> <i>f</i>, <i>þæt</i> <i>n</i>, <i>þā</i> <i>p</i>); <i>sē</i> is from Proto-West Germanic <i>*siz</i>, from Proto-Germanic <i>*sa</i>, ultimately from Proto-Indo-European <i>*só</i>.",  # noqa
                "Cognate with Saterland Frisian <i>die</i> (“the”), West Frisian <i>de</i> (“the”), Dutch <i>de</i> (“the”), German Low German <i>de</i> (“the”), German <i>der</i> (“the”), Danish <i>de</i> (“the”), Swedish <i>de</i> (“the”), Icelandic <i>sá</i> (“that”) within Germanic and with Sanskrit <i>sá</i> (“the, that”), Ancient Greek <i>ὁ</i> (“the”), Tocharian B <i>se</i> (“this”) among other Indo-European languages.",  # noqa
            ],
            [
                "<i>Definite grammatical article that implies necessarily that an entity it hints at is presupposed; something already mentioned, or completely specified later in that same sentence, or assumed already completely specified.</i> <small>[from 10th c.]</small>",  # noqa
                "<i>Used before a noun modified by a restrictive relative clause, indicating that the noun refers to a single referent defined by the relative clause.</i>",  # noqa
                "<i>Used before an object considered to be unique, or of which there is only one at a time.</i> <small>[from 10th c.]</small>",  # noqa
                "<i>Used before a superlative or an ordinal number modifying a noun, to indicate that the noun refers to a single item.</i>",  # noqa
                "<i>Added to a superlative or an ordinal number to make it into a substantive.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Introducing a singular term to be taken generically: preceding a name of something standing for a whole class.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Used before an adjective, indicating all things (especially persons) described by that adjective.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Used to indicate a certain example of (a noun) which is usually of most concern or most common or familiar.</i> <small>[from 12th c.]</small>",  # noqa
                "<i>Used before a body part (especially of someone previously mentioned), as an alternative to a possessive pronoun.</i> <small>[from 12th c.]</small>",  # noqa
                "<i>When stressed, indicates that it describes an object which is considered to be best or exclusively worthy of attention.</i> <small>[from 18th c.]</small>",  # noqa
                "<i>With a comparative or with <i>more</i> and a verb phrase, establishes a correlation with one or more other such comparatives.</i>",  # noqa
                "<i>With a comparative, and often with <i>for it</i>, indicates a result more like said comparative. This can be negated with <i>none</i>.</i>",  # noqa
                "For each; per.",
            ],
            [],
        ),
        (
            "um",
            ["/əːm/", "/ʌm/"],
            ["Onomatopoeic."],
            [
                "<i>Expression of hesitation, uncertainty or space filler in conversation</i>. See uh.",
                "<i>(chiefly US)</i> <i>Dated spelling of</i> <b>mmm</b>.",
                "<i>(intransitive)</i> To make the <i>um</i> sound to express uncertainty or hesitancy.",
                "<i>Alternative form of</i> <b>umbe</b>",
                "<i>(dated, sometimes humorous, often offensive)</i> <i>An undifferentiated determiner or article; a miscellaneous linking word, or filler with nonspecific meaning; representation of broken English stereotypically or comically attributed to Native Americans.</i>",  # noqa
            ],
            [],
        ),
        (
            "us",
            ["/əs/", "/əz/", "/ʌs/", "/ʌz/"],
            [
                "From Middle English <i>us</i>, from Old English <i>ūs</i> (“us”, dative personal pronoun), from Proto-Germanic <i>*uns</i> (“us”), from Proto-Indo-European <i>*ne-</i>, <i>*nō-</i>, <i>*n-ge-</i>, <i>*n̥smé</i> (“us”). Cognate with Saterland Frisian <i>uus</i> (“us”), West Frisian <i>us</i>, <i>ús</i> (“us”), Low German <i>us</i> (“us”), Dutch <i>ons</i> (“us”), German <i>uns</i> (“us”), Danish <i>os</i> (“us”), Latin <i>nōs</i> (“we, us”)."  # noqa
            ],
            [
                "<i>(personal)</i> Me and at least one other person; the objective case of <b>we</b>.",
                "<i>(Commonwealth, colloquial, chiefly with <i>give</i>)</i> Me.",
                "<i>(Northern England)</i> Our.",
                "<i>(Geordie)</i> Me (in all contexts).",
                "The speakers/writers, or the speaker/writer and at least one other person.",
                "<i>Alternative spelling of</i> <b>µs</b>: microsecond",
                "<i>(rare)</i> <i>Alternative form of</i> <b>u's</b>.",
            ],
            [],
        ),
        (
            "water",
            [
                "/ˈwoːtə/",
                "/ˈwætəɹ/",
                "/ˈwɑtəɹ/",
                "/ˈwɒtə/",
                "/ˈwɒtəɹ/",
                "/ˈwɔtər/",
                "/ˈwɔtəɹ/",
                "/ˈwɔːtə/",
                "/ˈwʊtəɹ/",
            ],
            [
                "From Middle English <i>water</i>, from Old English <i>wæter</i> (“water”), from Proto-West Germanic <i>*watar</i>, from Proto-Germanic <i>*watōr</i> (“water”), from Proto-Indo-European <i>*wódr̥</i> (“water”).",  # noqa
                "Cognate with cf, North Frisian <i>weeter</i> (“water”), Saterland Frisian <i>Woater</i> (“water”), West Frisian <i>wetter</i> (“water”), Dutch <i>water</i> (“water”), Low German <i>Water</i> (“water”), German <i>Wasser</i>, Old Norse <i>vatn</i> (Swedish <i>vatten</i> (“water”), Danish <i>vand</i> (“water”), Norwegian Bokmål <i>vann</i> (“water”), Norwegian Nynorsk and Icelandic <i>vatn</i> (“water”), Old Irish <i>coin fodorne</i> (“otters”, literally “water-dogs”), Latin <i>unda</i> (“wave”), Lithuanian <i>vanduõ</i> (“water”), Russian <i>вода́</i> (<i>voda</i>, “water”), Albanian <i>ujë</i> (“water”), Ancient Greek <i>ὕδωρ</i> (“water”), Armenian <i>գետ</i> (<i>get</i>, “river”), Sanskrit <i>उदन्</i> (<i>udán</i>, “wave, water”), Hittite <i>𒉿𒀀𒋻</i> (<i>wa-a-tar</i>).",  # noqa
            ],
            [
                "<i>(uncountable)</i> A substance (of molecular formula H<sub>2</sub>O) found at room temperature and pressure as a clear liquid; it is present naturally as rain, and found in rivers, lakes and seas; its solid form is ice and its gaseous form is steam.",  # noqa
                (
                    "<i>(uncountable, in particular)</i> The liquid form of this substance: liquid H<sub>2</sub>O.",
                    "<i>(countable)</i> A serving of liquid water.",
                ),
                "<i>(alchemy, philosophy)</i> The aforementioned liquid, considered one of the Classical elements or basic elements of alchemy.",  # noqa
                "<i>(uncountable or in the plural)</i> Water in a body; an area of open water.",
                "<i>(poetic, archaic or dialectal)</i> A body of water, almost always a river.",
                "A combination of water and other substance(s).",
                (
                    "<i>(sometimes countable)</i> Mineral water.",
                    "<i>(countable, often in the plural)</i> Spa water.",
                    "<i>(pharmacy)</i> A solution in water of a gaseous or readily volatile substance.",
                    "Urine. <small>[from 15th c.]</small>",
                    'Amniotic fluid or the amniotic sac containing it. (<i>Used only in the plural in the UK but often also in the singular in North America. (The Merriam-Webster Medical Dictionary says "often used in plural; also: bag of waters".)</i>)',  # noqa
                    "<i>(colloquial, medicine)</i> Fluids in the body, especially when causing swelling.",
                ),
                "<i>(figuratively, in the plural or in the singular)</i> A state of affairs; conditions; usually with an adjective indicating an adverse condition.",  # noqa
                "<i>(colloquial, figuratively)</i> A person's intuition.",
                "<i>(uncountable, dated, finance)</i> Excess valuation of securities.",
                "The limpidity and lustre of a precious stone, especially a diamond.",
                "A wavy, lustrous pattern or decoration such as is imparted to linen, silk, metals, etc.",
                "<i>(transitive)</i> To pour water into the soil surrounding (plants).",
                "<i>(transitive)</i> To wet or supply with water; to moisten; to overflow with water; to irrigate.",
                "<i>(transitive)</i> To provide (animals) with water for drinking.",
                "<i>(intransitive)</i> To get or take in water.",
                "<i>(transitive, colloquial)</i> To urinate onto.",
                "<i>(transitive)</i> To dilute.",
                "<i>(transitive, dated, finance)</i> To overvalue (securities), especially through deceptive accounting.",  # noqa
                "<i>(intransitive)</i> To fill with or secrete water.",
                "<i>(transitive)</i> To wet and calender, as cloth, so as to impart to it a lustrous appearance in wavy lines; to diversify with wavelike lines.",  # noqa
            ],
            [],
        ),
        (
            "word",
            ["/wɜːd/", "/wɝd/"],
            [
                "From Middle English <i>word</i>, from Old English <i>word</i>, from Proto-West Germanic <i>*word</i>, from Proto-Germanic <i>*wurdą</i>, from Proto-Indo-European <i>*wr̥dʰh₁om</i>. Doublet of <i>verb</i> and <i>verve</i>; further related to <i>vrata</i>."  # noqa
            ],
            [
                "The smallest unit of language that has a particular meaning and can be expressed by itself; the smallest discrete, meaningful unit of language. (<i>contrast <i>morpheme</i>.</i>)",  # noqa
                (
                    "The smallest discrete unit of spoken language with a particular meaning, composed of one or more phonemes and one or more morphemes",  # noqa
                    "The smallest discrete unit of written language with a particular meaning, composed of one or more letters or symbols and one or more morphemes",  # noqa
                    "A discrete, meaningful unit of language approved by an authority or native speaker (<i>compare non-word</i>).",  # noqa
                ),
                "Something like such a unit of language:",
                (
                    "A sequence of letters, characters, or sounds, considered as a discrete entity, though it does not necessarily belong to a language or have a meaning",  # noqa
                    "<i>(telegraphy)</i> A unit of text equivalent to five characters and one space. <small>[from 19th c.]</small>",  # noqa
                    "<i>(computing)</i> A fixed-size group of bits handled as a unit by a machine and which can be stored in or retrieved from a typical register (so that it has the same size as such a register). <small>[from 20th c.]</small>",  # noqa
                    "<i>(computer science)</i> A finite string that is not a command or operator. <small>[from 20th or 21st c.]</small>",  # noqa
                    "<i>(group theory)</i> A group element, expressed as a product of group elements.",
                ),
                "The fact or act of speaking, as opposed to taking action. <small>[from 9th c]</small>.",
                "<i>(now rare outside certain phrases)</i> Something that someone said; a comment, utterance; speech. <small>[from 10th c.]</small>",  # noqa
                "<i>(obsolete outside certain phrases)</i> A watchword or rallying cry, a verbal signal (even when consisting of multiple words).",  # noqa
                "<i>(obsolete)</i> A proverb or motto.",
                "<i>(uncountable)</i> News; tidings <small>[from 10th c.]</small>",
                "An order; a request or instruction; an expression of will. <small>[from 10th c.]</small>",
                "A promise; an oath or guarantee. <small>[from 10th c.]</small>",
                "A brief discussion or conversation. <small>[from 15th c.]</small>",
                "<i>(meiosis)</i> A minor reprimand.",
                "<i>(in the plural)</i> <i>See</i> <b>words</b>.",
                "<i>(theology, sometimes <b>Word</b>)</i> Communication from God; the message of the Christian gospel; the Bible, Scripture. <small>[from 10th c.]</small>",  # noqa
                "<i>(theology, sometimes <b>Word</b>)</i> Logos, Christ. <small>[from 8th c.]</small>",
                "<i>(transitive)</i> To say or write (something) using particular words; to phrase (something).",
                "<i>(transitive, obsolete)</i> To flatter with words, to cajole.",
                "<i>(transitive)</i> To ply or overpower with words.",
                "<i>(transitive, rare)</i> To conjure with a word.",
                "<i>(intransitive, archaic)</i> To speak, to use words; to converse, to discourse.",
                "<i>Alternative form of</i> <b>worth</b> (“to become”).",
                '<i>(slang, African-American Vernacular)</i> Truth, indeed, that is the truth! The shortened form of the statement "My word is my bond."',  # noqa
                "<i>(slang, emphatic, stereotypically, African-American Vernacular)</i> An abbreviated form of <i>word up</i>; a statement of the acknowledgment of fact with a hint of nonchalant approval.",  # noqa
            ],
            [],
        ),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: List[str],
    etymology: List[Definitions],
    definitions: List[Definitions],
    variants: List[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "en")
    details = parse_word(word, code, "en", force=True)
    assert pronunciations == details.pronunciations
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{1|influenza}}", "Influenza"),
        ("{{abbr of|en|abortion}}", "<i>Abbreviation of</i> <b>abortion</b>."),
        ("{{abbreviation of|en|abortion}}", "<i>Abbreviation of</i> <b>abortion</b>."),
        (
            "{{alt case|en|angstrom}}",
            "<i>Alternative letter-case form of</i> <b>angstrom</b>",
        ),
        ("{{alt form|enm|theen}}", "<i>Alternative form of</i> <b>theen</b>"),
        (
            "{{alt form|enm|a|pos=indefinite article}}",
            "<i>Alternative form of</i> <b>a</b> (indefinite article)",
        ),
        (
            "{{alt form|enm|worth|t=to become}}",
            "<i>Alternative form of</i> <b>worth</b> (“to become”)",
        ),
        (
            "{{alternative form of|enm|theen}}",
            "<i>Alternative form of</i> <b>theen</b>",
        ),
        (
            "{{alternative spelling of|en|µs}}",
            "<i>Alternative spelling of</i> <b>µs</b>",
        ),
        ("{{C.|20}}", "20th c."),
        ("{{C.|21|st}}", "21st c."),
        ("{{circa2|1850s}}", "<i>circa</i> 1850s"),
        ("{{circa2|1955–1956|short=yes}}", "<i>c.</i> 1955–1956"),
        ("{{clipping of|en|yuppie}}", "<i>Clipping of</i> <b>yuppie</b>."),
        ("{{defdate|from 15th c.}}", "<small>[from 15th c.]</small>"),
        ("{{eye dialect of|en|is}}", "<i>Eye dialect spelling of</i> <b>is</b>."),
        (
            "{{form of|en|obsolete emphatic|ye}}",
            "<i>obsolete emphatic of</i> <b>ye</b>",
        ),
        ("{{gloss|liquid H<sub>2</sub>O}}", "(liquid H<sub>2</sub>O)"),
        ("{{glossary|inflected}}", "inflected"),
        ("{{glossary|inflected|Inflected}}", "Inflected"),
        (
            "{{initialism of|en|Inuit Qaujimajatuqangit|nodot=1}}",
            "<i>Initialism of</i> <b>Inuit Qaujimajatuqangit</b>",
        ),
        ("{{IPAfont|ʌ}}", "⟨ʌ⟩"),
        (
            "{{Latn-def|en|name|O|o}}",
            "<i>The name of the Latin-script letter</i> <b>O</b>.",
        ),
        (
            "{{n-g|Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{ngd|Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{non-gloss definition|Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{non-gloss definition|1=Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{q|formal|used only in the plural}}",
            "(<i>formal</i>, <i>used only in the plural</i>)",
        ),
        (
            "{{qual|Used only in the plural in the UK}}",
            "(<i>Used only in the plural in the UK</i>)",
        ),
        (
            "{{qualifier|Used only in the plural in the UK}}",
            "(<i>Used only in the plural in the UK</i>)",
        ),
        ("{{sense|man of beastly nature}}", "(<i>man of beastly nature</i>) :"),
        ("{{smc|ah}}", "<span style='font-variant:small-caps'>ah</span>"),
        ("{{sub|KI}}", "<sub>KI</sub>"),
        ("{{sup|KI}}", "<sup>KI</sup>"),
        ("{{synonym of|en|drip tip}}", "<i>Synonym of</i> <b>drip tip</b>"),
        (
            "{{taxfmt|Gadus macrocephalus|species|ver=170710}}",
            "<i>Gadus macrocephalus</i>",
        ),
        (
            "{{taxlink|Gadus macrocephalus|species|ver=170710}}",
            "<i>Gadus macrocephalus</i>",
        ),
        ("{{uder|en|fro|jargon}}", "Old French <i>jargon</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "en") == expected
