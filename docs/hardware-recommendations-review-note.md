# Hardware recommendations - review note

Reefy manages computers and apps that users own or are authorized to manage.
It provides a complete device/app workflow independently of hardware purchases.

During first-computer onboarding, the setup skill asks whether the user already
has a compatible computer and USB drive. Existing suitable hardware skips
shopping. Only users seeking hardware suggestions receive optional examples of
Reefy-tested configurations. Users can obtain compatible hardware from any retailer.

The examples link to ordinary third-party product pages. Reefy does not sell
these recommended products, handle orders, collect payment information or process
their payments. The plugin does not embed checkout or automatically purchase
hardware. The guide labels example prices as approximate, not current offers,
and directs users to check the selected configuration and current availability.
Product prices are not advertised in directory listing metadata.

The product URLs use canonical Amazon product identifiers without the original
share-link query parameters. Resolving a product identifier is not verification
of current stock, pricing or every selectable hardware variant. The skill must
not imply that OpenAI endorses a recommendation or that purchasing a listed
product is required to use Reefy.

## Review context

This note describes the shipped recommendation behavior and is suitable for
adapting into review explanations. It is not an assertion of OpenAI approval.
OpenAI permits physical-goods commerce and prohibits advertising-focused plugins.
Its checkout guidance does not expressly resolve this optional third-party
hardware-reference case. Disclose the recommendations to reviewers rather than
claiming an exception to checkout policy.

Reference: https://developers.openai.com/plugins/plugin-guidelines
