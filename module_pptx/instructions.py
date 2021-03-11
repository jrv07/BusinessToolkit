from module_pptx.PptxContentPage import PptxContentPage
from module_pptx.PptxContactPage import PptxContactPage
from module_pptx.PptxTitlePage import PptxTitlePage
from module_pptx.PptxInstructionFactory import PptxInstructionFactory
from module_pptx.PptxMovieInstruction import PptxMovieInstruction
from module_pptx.PptxPictureInstruction import PptxPictureInstruction
from module_pptx.PptxPresentation import PptxPresentation
from module_pptx.PptxSlideCreationFactory import PptxSlideCreationFactory
from module_pptx.PptxTextboxInstruction import PptxTextboxInstruction
from module_pptx.PptxTableFromDataInstruction import PptxTableFromDataInstruction
from module_pptx.PptxTableManualInstruction import PptxTableManualInstruction
from module_pptx.PptxTextContentEntry import PptxTextContentEntry
from module_pptx.pptx_table.PptxTableFactory import PptxTableFactory
from module_pptx.pptx_table.PptxTableCellFactory import PptxTableCellFactory
from module_pptx.pptx_table.PptxTableRow import PptxTableRow
from module_pptx.pptx_table.PptxTableStyleCellDefinition import PptxTableStyleCellDefinition
from module_pptx.pptx_table.PptxTableStyleColumnDefinition import PptxTableStyleColumnDefinition
from module_pptx.pptx_table.PptxTableStyleDefinitions import PptxTableStyleDefinitions
from module_pptx.pptx_table.PptxTableStyleRowDefinition import PptxTableStyleRowDefinition
from module_pptx.pptx_table.PptxTableTextCell import PptxTableTextCell
from module_pptx.pptx_table.PptxTableThresholdsCell import PptxTableThresholdsCell
from module_pptx.pptx_styles.PptxCellStyle import PptxCellStyle
from module_pptx.pptx_styles.PptxParagraphStyle import PptxParagraphStyle
from module_pptx.pptx_styles.PptxRunStyle import PptxRunStyle
from module_pptx.pptx_styles.PptxTextFrameStyle import PptxTextFrameStyle
from module_pptx.pptx_styles.PptxColor import PptxColor
from module_pptx.PptxShapeBorder import PptxShapeBorder
from module_pptx.PptxFromVariable import PptxFromVariable

instructions = [
    PptxTitlePage({}, None),
    PptxContactPage({}, None),
    PptxContentPage({}, None),
    PptxInstructionFactory({}, None),
    PptxPictureInstruction({}, None),
    PptxMovieInstruction({}, None),
    PptxPresentation({}),
    PptxSlideCreationFactory({}, None),
    PptxTextboxInstruction({}, None),
    PptxTableFromDataInstruction({}, None),
    PptxTableManualInstruction({}, None),
    PptxTextContentEntry({}, None, None),
    PptxTableFactory({}),
    PptxTableCellFactory({}, None),
    PptxTableRow({}, None),
    PptxTableStyleCellDefinition({}),
    PptxTableStyleColumnDefinition({}),
    PptxTableStyleDefinitions({}),
    PptxTableStyleRowDefinition({}),
    PptxTableTextCell({}, None),
    PptxTableThresholdsCell({}, None),
    PptxCellStyle({}),
    PptxParagraphStyle({}),
    PptxRunStyle({}),
    PptxTextFrameStyle({}),
    PptxColor({}),
    PptxShapeBorder({}),
    PptxFromVariable({})
]
