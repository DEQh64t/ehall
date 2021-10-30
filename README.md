# ehall

Ehall is a tiny command-line utility to access [Ehall·of·NanJing·Medical·University](http://ehall.njmu.edu.cn) in case there is no other handy way to do it.

Interested? [Install it](#installation) now and [get started by examples](#getting-started).

## Installation

### Prerequisites

- **Python**

- **Pandoc**

### Git clone

```bash
git clone https://github.com/DEQh64t/ehall.git
```

Then run `pip install -r requirements.txt` to get things ready.

## Getting Started

### 学生科研日志

#### Example

```markdown
---
title: Title
txrq: 2021-09-01 09:00:00
---

# Heading 1
## Heading 2

Hello, World!

...
```

Between these triple-dashed lines, you can set predefined variables (see below for a reference).

| VARIABLE | DESCRIPTION |
| -------- | ----------- |
| title    | 标题        |
| txrq     | 填写日期    |

You can save it directly with:

```python
from ehall.njmu.yjsyss import Yjsyss
yjsyss = Yjsyss(username, password)
yjsyss.save_record_from_file(filename)
```

### 学生讲座报名

You can register it directly with:

```python
from ehall.njmu.yjsyss import Yjsyss
yjsyss = Yjsyss(username, password)
yjsyss.get_lectures()
yjsyss.register_lecture_by_id(id)
```

## Legal Issues

This software is distributed under the [MIT license](https://github.com/DEQh64t/ehall/raw/dev/LICENSE).

In particular, please be aware that

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Translated to human words:

*In case your use of the software forms the basis of copyright infringement, or you use the software for any other illegal purposes, the authors cannot take any responsibility for you.*

We only ship the code here, and how you are going to use it is left to your own discretion.

## Authors

Made by [@DEQh64t](https://github.com/DEQh64t), who is in turn powered by :coffee:, :beer: and :ramen:.

You can find the [list of all contributors](https://github.com/DEQh64t/ehall/graphs/contributors) here.
